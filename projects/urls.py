from django.urls import path

from users.views import WorkerListView
from .views import ProjectCreateView
from .views import ProjectDeleteView
from .views import ProjectDetailView
from .views import ProjectListView
from .views import ProjectUpdateView

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
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="update-project"
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="delete-project"
    ),
    path(
        "projects/<int:pk>/detail",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
]

app_name = "projects"
