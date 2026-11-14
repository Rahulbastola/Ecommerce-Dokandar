
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="api_register"),
    path("login/", views.login, name="api_login"),
]
