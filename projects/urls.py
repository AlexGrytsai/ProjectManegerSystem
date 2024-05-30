from django.urls import path

from projects.views import CommentCreatView
from projects.views import CommentDeleteView
from projects.views import CommentUpdateView
from projects.views import ProjectCreateView
from projects.views import ProjectDeleteView
from projects.views import ProjectDetailTasksView
from projects.views import ProjectDetailView
from projects.views import ProjectListView
from projects.views import ProjectUpdateView
from projects.views import TaskCreateView
from projects.views import TaskDeleteView
from projects.views import TaskDetailView
from projects.views import TaskListView
from projects.views import TaskUpdateView
from users.views import WorkerListView
from users.views import toggle_assign_to_task

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
        "projects/<int:pk>/detail/",
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
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/comments/create/",
        CommentCreatView.as_view(),
        name="comment-create",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:task_id>/comments/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:task_id>/comments/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]

app_name = "projects"
