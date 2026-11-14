
from django.urls import path
from . import website_views

urlpatterns = [
    path("register/", website_views.register, name="register"),
    path("login/", website_views.website_login, name="login"),
    path("logout/", website_views.website_logout, name="logout"),
    path("profile/", website_views.profile, name="profile"),
    path("profile/edit/", website_views.edit_profile, name="edit_profile"),
]
