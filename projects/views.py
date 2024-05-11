from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from view_breadcrumbs import BaseBreadcrumbMixin
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from .models import Project
from .forms import ProjectCreateForm


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

    def test_func(self):
        return self.request.user.role == "Supervisor"

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        context["is_update"] = True
        return context

    def get_success_url(self):
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

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        total_projects = Project.objects.all().count()
        context["total_workers"] = total_projects

        for project in context["project_list"]:
            project.tasks_in_progress_count = project.tasks.exclude(
                status="Done"
            ).count
            project.tasks_done_count = project.tasks.filter(
                status="Done"
            ).count
            project.responsible_workers_count = (
                project.responsible_workers.count()
            )
        return context
