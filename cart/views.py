
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import products


def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = get_object_or_404(products, id=int(product_id))
        quantity = int(quantity)
        subtotal = product.price * quantity

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal
    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total,
    })


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(products, id=product_id)
    cart = request.session.get('cart', {})
    key = str(product.id)
    quantity = int(cart.get(key, 0))

    if product.stock > quantity:
        cart[key] = quantity + 1
        request.session['cart'] = cart

    return redirect('cart_detail')


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart

    return redirect('cart_detail')


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(products, id=product_id)
    cart = request.session.get('cart', {})
    key = str(product.id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        return redirect('cart_detail')

    if quantity <= 0:
        cart.pop(key, None)
    elif quantity <= product.stock:
        cart[key] = quantity

    request.session['cart'] = cart
    return redirect('cart_detail')
