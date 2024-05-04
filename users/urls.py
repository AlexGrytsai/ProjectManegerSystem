from django.urls import include
from django.urls import path

from .views import IndexView
from .views import ProfileView
from .views import RegisterView
from .views import WorkerDetailView
from .views import WorkerUpdateView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", IndexView.as_view(), name="index"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register-user"),
    path(
        "accounts/profile/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "accounts/profile/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
]

app_name = "users"
