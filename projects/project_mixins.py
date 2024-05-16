from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from projects.models import Project


class TaskMixin:
    def get_project(self) -> Project:
        if not hasattr(self, "_project"):
            project_id = self.kwargs.get("project_id")
            self._project = get_object_or_404(Project, id=project_id)

        return self._project

    def check_responsible_worker(self) -> bool:
        project = self.get_context_data().get("project")

        return self.request.user in project.responsible_workers.all()

    def get_success_url(self) -> str:
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy(
            "projects:task-list", args=[self.kwargs.get("project_id")]
        )
