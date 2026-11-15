
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import products
from .models import Cart, Order, OrderItem
from .serializer import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Customers can only access their own orders.
        return Order.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = list(cart.items.select_related("product").all())

        if not cart_items:
            return Response(
                {"error": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                total_amount = Decimal("0.00")

                for item in cart_items:
                    if item.quantity < 1 or item.quantity > item.product.stock:
                        return Response(
                            {
                                "error": (
                                    f"Not enough stock for "
                                    f"{item.product.name}."
                                )
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    total_amount += item.product.price * item.quantity

                order = Order.objects.create(
                    customer=request.user,
                    customer_name=(
                        request.data.get("customer_name")
                        or request.user.username
                    ),
                    phone=request.data.get("phone", ""),
                    delivery_address=request.data.get(
                        "delivery_address", ""
                    ),
                    total_amount=total_amount,
                    status="Pending"
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                    item.product.stock -= item.quantity
                    item.product.save(update_fields=["stock"])

                cart.items.filter(
                    id__in=[item.id for item in cart_items]
                ).delete()

        except Exception:
            return Response(
                {"error": "Could not place the order. Please try again."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializer(order)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


# WEBSITE CHECKOUT
@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    if request.method == "POST":
        customer_name = request.POST.get(
            "customer_name", ""
        ).strip()
        phone = request.POST.get("phone", "").strip()
        delivery_address = request.POST.get(
            "delivery_address", ""
        ).strip()

        if not customer_name or not phone or not delivery_address:
            messages.error(
                request,
                "Please complete all delivery details."
            )
            return redirect("checkout")

        try:
            with transaction.atomic():
                order_items = []
                total = Decimal("0.00")

                for product_id, quantity in cart.items():
                    product = products.objects.get(
                        id=int(product_id)
                    )
                    quantity = int(quantity)

                    if quantity < 1 or quantity > product.stock:
                        raise ValueError(
                            f"Invalid quantity or insufficient stock "
                            f"for {product.name}."
                        )

                    order_items.append((product, quantity))
                    total += product.price * quantity

                order = Order.objects.create(
                    customer=request.user,
                    customer_name=customer_name,
                    phone=phone,
                    delivery_address=delivery_address,
                    total_amount=total,
                    status="Pending"
                )

                for product, quantity in order_items:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )

                    product.stock -= quantity
                    product.save(update_fields=["stock"])

        except (ValueError, TypeError, products.DoesNotExist):
            messages.error(
                request,
                "An item is unavailable or its quantity is invalid. "
                "Please review your cart."
            )
            return redirect("cart_detail")

        # Clear the cart after the order is successfully saved.
        request.session["cart"] = {}

        # Show the order confirmation page.
        return redirect("order_success", order_id=order.id)

    return render(request, "orders/checkout.html")


# WEBSITE ORDER SUCCESS PAGE
@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    return render(
        request,
        "orders/order_success.html",
        {"order": order}
    )
# CUSTOMER ORDER HISTORY
@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(customer=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    return render(
        request,
        "orders/my_orders.html",
        {"orders": orders}
    )
