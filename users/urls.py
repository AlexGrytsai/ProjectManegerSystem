from django.urls import path
from django.urls import include

from .views import IndexView
from .views import ProfileView
from .views import RegisterView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", IndexView.as_view(), name="index"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register-user"),
]

app_name = "users"
