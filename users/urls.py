from django.urls import include
from django.urls import path

from .views import (
    IndexView,
    AddWorkerView,
    RegisterView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerListView,
)

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register-user"),
    path("addworker/", AddWorkerView.as_view(), name="add-worker"),
    path(
        "accounts/profile/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "accounts/profile/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
]

app_name = "users"
