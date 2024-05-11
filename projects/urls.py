from django.urls import include
from django.urls import path

from .views import ProjectCreateView
from .views import ProjectListView

urlpatterns = [
    path("projects/create/",
         ProjectCreateView.as_view(),
         name="create-project"),
    path("projects/list", ProjectListView.as_view(), name="project-list"),
]

app_name = "projects"
