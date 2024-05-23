from django.shortcuts import get_object_or_404

from projects.models import Project
from projects.models import Task


class TaskMixin:
    def get_project(self) -> Project:
        if not hasattr(self, "_project"):
            project_id = self.kwargs.get("project_id")
            self._project = get_object_or_404(Project, id=project_id)

        return self._project

    def get_task(self, name_id: str) -> Task:
        if not hasattr(self, "_task"):
            task_id = self.kwargs.get(name_id)
            self._task = get_object_or_404(Task, id=task_id)

        return self._task

    def check_responsible_worker(self) -> bool:
        project = self.get_project()

        return self.request.user in project.responsible_workers.all()
