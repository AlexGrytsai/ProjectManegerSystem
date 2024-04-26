from django.urls import path
from django.urls import include
from django.contrib.auth.views import LogoutView

from .views import IndexView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("", IndexView.as_view(), name="index"),
]

app_name = "users"
