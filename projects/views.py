from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
from django.http import HttpResponseRedirect
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
from .forms import TaskUpdateForm
from .models import Project, TackStatus
from .models import Task
from .project_mixins import TaskMixin


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

    @transaction.atomic
    def form_valid(self, form) -> HttpResponseRedirect:
        form.instance.project_lead = self.request.user
        result = super(ProjectCreateView, self).form_valid(form)
        form.instance.responsible_workers.add(self.request.user)
        return result

    def get_context_data(self, **kwargs) -> dict:
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
                "tasks",
                filter=~Q(tasks__status=TackStatus.DONE),
                distinct=True
            ),
            tasks_done_count=Count(
                "tasks",
                filter=Q(tasks__status=TackStatus.DONE),
                distinct=True
            ),
            responsible_workers_count=Count(
                "responsible_workers", distinct=True
            ),
            project_lead_username=F("project_lead__username"),
            project_lead_first_name=F("project_lead__first_name"),
            project_lead_last_name=F("project_lead__last_name"),
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super(ProjectListView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
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

    def get_context_data(self, **kwargs) -> dict:
        context = super(ProjectDeleteView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    queryset = Project.objects.select_related("project_lead").prefetch_related(
        "responsible_workers", "tasks"
    )

    def get_context_data(self, **kwargs) -> dict:
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        return context


class ProjectDetailTasksView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_task_list.html"
    queryset = Project.objects.prefetch_related(
        "tasks",
        "tasks__responsible_workers"
    )

    def get_context_data(self, **kwargs) -> dict:
        context = super(ProjectDetailTasksView, self).get_context_data(
            **kwargs
        )
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "projects/task_list.html"
    context_object_name = "task_list"

    queryset = Task.objects.prefetch_related(
        "project_tasks", "responsible_workers"
    )

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url

        return context


class TaskCreateView(
    LoginRequiredMixin,
    TaskMixin,
    UserPassesTestMixin,
    CreateView
):
    model = Task
    form_class = TaskCreateForm
    template_name = "projects/task_form.html"

    def test_func(self) -> bool:
        return (
                self.request.user.role == "Supervisor" or
                self.check_responsible_worker()
        )

    @transaction.atomic
    def form_valid(self, form) -> HttpResponseRedirect:
        form.instance.author = self.request.user
        result = super(TaskCreateView, self).form_valid(form)
        form.instance.responsible_workers.add(self.request.user)

        project = self.get_project()
        project.tasks.add(form.instance)
        return result

    def get_form_kwargs(self) -> dict[str, dict]:
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs["project"] = self.get_project()
        return kwargs

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        project = self.get_project()
        context["project"] = project
        return context

    def get_success_url(self) -> str:
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy(
            "projects:task-list", args=[self.kwargs.get("project_id")]
        )


class TaskUpdateView(
    LoginRequiredMixin,
    TaskMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Task
    form_class = TaskUpdateForm
    template_name = "projects/task_form.html"

    def test_func(self) -> bool:
        return (
                self.request.user.role == "Supervisor" or
                self.check_responsible_worker()
        )

    def get_form_kwargs(self) -> dict[str, dict]:
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs["user_role"] = self.request.user.role
        kwargs["project"] = self.get_project()
        return kwargs

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskUpdateView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        project = self.get_project()
        context["project"] = project
        context["is_update"] = True
        return context

    def get_success_url(self) -> str:
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy(
            "projects:task-list", args=[self.kwargs.get("project_id")]
        )


class TaskDeleteView(
    LoginRequiredMixin,
    TaskMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Task
    template_name = "projects/task_confirm_delete.html"
    success_url = reverse_lazy("projects:task-list")

    def test_func(self):
        return (
                self.request.user.role == "Supervisor"
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskDeleteView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        return context

    def get_success_url(self) -> str:
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy(
            "projects:task-list"
        )


class TaskDetailView(
    LoginRequiredMixin,
    TaskMixin,
    UserPassesTestMixin,
    DetailView
):
    model = Task
    template_name = "projects/task_detail.html"
    context_object_name = "task"
    queryset = Task.objects.select_related("author").prefetch_related(
        "responsible_workers"
    )

    def test_func(self):
        return (
                self.request.user.role == "Supervisor" or
                self.check_responsible_worker()
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        project = self.get_project()
        context["project"] = project
        return context
