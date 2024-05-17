from django.urls import path

from users.views import WorkerListView
from .views import ProjectCreateView
from .views import ProjectDeleteView
from .views import ProjectDetailTasksView
from .views import ProjectDetailView
from .views import ProjectListView
from .views import ProjectUpdateView
from .views import TaskCreateView
from .views import TaskDeleteView
from .views import TaskListView
from .views import TaskUpdateView

urlpatterns = [
    path("projects/create/",
         ProjectCreateView.as_view(),
         name="create-project"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
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
    path(
        "projects/<int:pk>/tasks-list/",
        ProjectDetailTasksView.as_view(),
        name="project-task-list"
    ),
    path(
        "projects/<int:project_id>/tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "projects/tasks/",
        TaskListView.as_view(),
        name="task-list"
    )
    # path(
    #     "projects/<int:project_id>/tasks/<int:pk>/toggle-assign/",
    #     toggle_assign_to_task,
    #     name="toggle-task-assign",
    # ),
]

app_name = "projects"
