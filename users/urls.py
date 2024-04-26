from django.urls import path
from django.urls import include

from .views import index_view

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", index_view, name="index"),
]

app_name = "users"
