from django.urls import include
from django.urls import path

from .views import IndexView
from .views import ProfileView
from .views import RegisterView
from .views import UserDetailView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", IndexView.as_view(), name="index"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register-user"),
    path(
        "accounts/profile/<int:pk>/",
        UserDetailView.as_view(),
        name="worker-detail"
    ),
]

app_name = "users"
