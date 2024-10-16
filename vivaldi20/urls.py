from django.urls import path, include
from .views import authView, home

urlpatterns = [
    path("", home, name="home"),
    path("register/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
]
