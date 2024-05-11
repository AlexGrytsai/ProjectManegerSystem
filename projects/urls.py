from django.urls import include
from django.urls import path

from .views import ProjectCreateView
from .views import ProjectListView
from users.views import WorkerListView

urlpatterns = [
    path("projects/create/",
         ProjectCreateView.as_view(),
         name="create-project"),
    path("projects/list", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<int:project_id>/workers/",
        WorkerListView.as_view(),
        name="project-workers"
    ),
]

app_name = "projects"
