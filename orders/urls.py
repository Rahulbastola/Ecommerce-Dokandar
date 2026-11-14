
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, checkout, order_success

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', checkout, name='checkout'),
    path('success/<int:order_id>/', order_success, name='order_success'),
]
