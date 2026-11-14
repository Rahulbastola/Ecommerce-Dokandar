
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    productsViewSet,
    CetegoryViewSet,
    product_list,
    product_detail,
    vendor_dashboard,
    product_create,
    product_edit,
    product_delete,
    category_list,
    category_create,
    category_edit,
    category_delete,
)

router = DefaultRouter()

router.register(
    r'products',
    productsViewSet,
    basename='products'
)

router.register(
    r'categories',
    CetegoryViewSet,
    basename='categories'
)

urlpatterns = [
    path('', include(router.urls)),

    # Customer shop
    path('shop/', product_list, name='product_list'),
    path('shop/<int:product_id>/', product_detail, name='product_detail'),

    # Vendor dashboard and products
    path('vendor/dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('vendor/products/add/', product_create, name='product_create'),
    path('vendor/products/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('vendor/products/<int:product_id>/delete/', product_delete, name='product_delete'),

    # Vendor categories
    path('vendor/categories/', category_list, name='category_list'),
    path('vendor/categories/add/', category_create, name='category_create'),
    path('vendor/categories/<int:category_id>/edit/', category_edit, name='category_edit'),
    path('vendor/categories/<int:category_id>/delete/', category_delete, name='category_delete'),
]
