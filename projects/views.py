from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from view_breadcrumbs import BaseBreadcrumbMixin

from .forms import ProjectCreateForm
from .forms import ProjectUpdateForm
from .forms import TaskCreateForm
from .models import Project
from .models import Task


class ProjectCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    BaseBreadcrumbMixin,
    CreateView
):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/project_form.html"

    crumbs = [
        ("", "Home"),
        ("Projects", reverse_lazy("projects:project-list")),
        ("Add new Worker", "")
    ]

    def test_func(self) -> bool:
        return self.request.user.role == "Supervisor"

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        context["is_update"] = True
        return context

    def get_success_url(self) -> str:
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("/")


class ProjectListView(LoginRequiredMixin, BaseBreadcrumbMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "project_list"
    queryset = Project.objects.prefetch_related("responsible_workers", "tasks")
    paginate_by = 10

    crumbs = [("", "Home"), ("Projects", "")]

    @staticmethod
    def get_annotate_params() -> dict:
        return Project.objects.annotate(
            tasks_in_progress_count=Count(
                "tasks", filter=~Q(tasks__status="In Progress")
            ),
            tasks_done_count=Count(
                "tasks", filter=Q(tasks__status="Done")
            ),
            responsible_workers_count=Count("responsible_workers"),
            project_lead_username=F("project_lead__username"),
            project_lead_first_name=F("project_lead__first_name"),
            project_lead_last_name=F("project_lead__last_name"),
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super(ProjectListView, self).get_context_data(**kwargs)
        total_projects = Project.objects.count()
        context["total_workers"] = total_projects

        annotate_params = self.get_annotate_params()

        context["project_list"] = annotate_params

        return context


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = "projects/project_form.html"

    def test_func(self) -> bool:
        return self.request.user.role == "Supervisor"

    def get_context_data(self, **kwargs) -> dict:
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        context["is_update"] = True
        return context

    def get_success_url(self) -> str:
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("projects:project-list")


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("projects:project-list")
    template_name = "projects/project_delete_confirm.html"

    def test_func(self) -> bool:
        return self.request.user.role == "Supervisor"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    queryset = Project.objects.select_related("project_lead").prefetch_related(
        "responsible_workers", "tasks"
    )


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "projects/task_list.html"
    context_object_name = "task_list"

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["project_id"] = self.kwargs.get("project_id")

        project = Project.objects.get(id=self.kwargs.get("project_id"))
        context["project_lead_id"] = project.project_lead_id

        return context


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "projects/task_form.html"

    def test_func(self) -> bool:
        return (
                self.request.user.role == "Supervisor" or
                self.check_responsible_worker()
        )

    def get_project(self) -> Project:
        try:
            project_id = self.kwargs.get("project_id")
            project = Project.objects.get(id=project_id)

            return project

        except Project.DoesNotExist:
            raise Http404("Project does not exist")

    def check_responsible_worker(self) -> bool:
        project = self.get_project()

        return self.request.user in project.responsible_workers.all()
