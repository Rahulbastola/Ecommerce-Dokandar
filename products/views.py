
from functools import wraps

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import products, Cetegory
from .serializer import productsSerializer, CetegorySerializer


# -------------------------
# Forms
# -------------------------

class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = [
            "name", "description", "price",
            "stock", "images", "cetegory",
        ]

    def __init__(self, *args, vendor=None, **kwargs):
        super().__init__(*args, **kwargs)

        if vendor is not None:
            self.fields["cetegory"].queryset = Cetegory.objects.filter(
                vendor=vendor
            )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Cetegory
        fields = ["name"]


# -------------------------
# API permissions
# -------------------------

class VendorProductPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "Vendor"
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.vendor_id == request.user.id


class productsViewSet(viewsets.ModelViewSet):
    serializer_class = productsSerializer
    permission_classes = [VendorProductPermission]

    def get_queryset(self):
        user = self.request.user

        if (
            user.is_authenticated
            and getattr(user, "role", None) == "Vendor"
        ):
            return products.objects.filter(vendor=user)

        return products.objects.all()

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    def perform_update(self, serializer):
        serializer.save(vendor=self.request.user)


class CetegoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cetegory.objects.all()
    serializer_class = CetegorySerializer


# -------------------------
# Vendor-only protection
# -------------------------

def vendor_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if getattr(request.user, "role", None) != "Vendor":
            messages.error(
                request,
                "Only vendor accounts can manage products and categories."
            )
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


# -------------------------
# Public shop
# -------------------------

def product_list(request):
    query = request.GET.get("q", "").strip()

    product_items = products.objects.select_related(
        "cetegory", "vendor"
    ).all()

    if query:
        product_items = product_items.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
        )

    return render(request, "products/product_list.html", {
        "products": product_items,
        "query": query,
    })


def product_detail(request, product_id):
    product = get_object_or_404(products, id=product_id)

    return render(request, "products/product_detail.html", {
        "product": product,
    })


# -------------------------
# Vendor dashboard
# -------------------------

@vendor_required
def vendor_dashboard(request):
    vendor_products = products.objects.filter(
        vendor=request.user
    ).select_related("cetegory")

    vendor_categories = Cetegory.objects.filter(
        vendor=request.user
    )

    return render(request, "products/vendor_dashboard.html", {
        "products": vendor_products,
        "categories": vendor_categories,
    })


# -------------------------
# Add product
# -------------------------

@vendor_required
def product_create(request):
    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        vendor=request.user,
    )

    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.vendor = request.user
        product.save()

        messages.success(request, "Product added successfully!")
        return redirect("vendor_dashboard")

    return render(request, "products/product_form.html", {
        "form": form,
        "page_title": "Add Product",
    })


# -------------------------
# Edit own product
# -------------------------

@vendor_required
def product_edit(request, product_id):
    product = get_object_or_404(
        products,
        id=product_id,
        vendor=request.user,
    )

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product,
        vendor=request.user,
    )

    if request.method == "POST" and form.is_valid():
        updated_product = form.save(commit=False)
        updated_product.vendor = request.user
        updated_product.save()

        messages.success(request, "Product updated successfully!")
        return redirect("vendor_dashboard")

    return render(request, "products/product_form.html", {
        "form": form,
        "page_title": "Edit Product",
    })


# -------------------------
# Delete own product
# -------------------------

@vendor_required
def product_delete(request, product_id):
    product = get_object_or_404(
        products,
        id=product_id,
        vendor=request.user,
    )

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("vendor_dashboard")

    return render(request, "products/product_confirm_delete.html", {
        "product": product,
    })


# -------------------------
# Category management
# -------------------------

@vendor_required
def category_list(request):
    categories = Cetegory.objects.filter(
        vendor=request.user
    ).order_by("name")

    return render(request, "products/category_list.html", {
        "categories": categories,
    })


@vendor_required
def category_create(request):
    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        category = form.save(commit=False)
        category.vendor = request.user
        category.save()

        messages.success(request, "Category created successfully!")
        return redirect("category_list")

    return render(request, "products/category_form.html", {
        "form": form,
        "page_title": "Add Category",
    })


@vendor_required
def category_edit(request, category_id):
    category = get_object_or_404(
        Cetegory,
        id=category_id,
        vendor=request.user,
    )

    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully!")
        return redirect("category_list")

    return render(request, "products/category_form.html", {
        "form": form,
        "page_title": "Edit Category",
    })


@require_POST
@vendor_required
def category_delete(request, category_id):
    category = get_object_or_404(
        Cetegory,
        id=category_id,
        vendor=request.user,
    )

    # Avoid deleting a category that is already used by products.
    if products.objects.filter(cetegory=category).exists():
        messages.error(
            request,
            "This category contains products. Move or delete those products first."
        )
        return redirect("category_list")

    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect("category_list")
