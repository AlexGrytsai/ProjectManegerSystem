from django.urls import path
from django.urls import include

from .views import IndexView
from .views import ProfileView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", IndexView.as_view(), name="index"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
]

app_name = "users"
