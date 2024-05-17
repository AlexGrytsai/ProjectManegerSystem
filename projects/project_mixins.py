from django.shortcuts import get_object_or_404

from projects.models import Project


class TaskMixin:
    def get_project(self) -> Project:
        if not hasattr(self, "_project"):
            project_id = self.kwargs.get("project_id")
            self._project = get_object_or_404(Project, id=project_id)

        return self._project

    def check_responsible_worker(self) -> bool:
        project = self.get_project()

        return self.request.user in project.responsible_workers.all()
