from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from view_breadcrumbs import BaseBreadcrumbMixin

from .forms import AddWorkerForm
from .forms import RegisterForm
from .forms import WorkerSearchForm
from .forms import WorkerUserUpdateForm
from .models import WorkerUser


class IndexView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = "index.html"
    crumbs = [("", "Home"), ]


class RegisterView(CreateView):
    model = WorkerUser
    form_class = RegisterForm
    template_name = "registration/register_form.html"

    success_url = reverse_lazy("users:login")


class AddWorkerView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    BaseBreadcrumbMixin,
    CreateView
):
    model = WorkerUser
    form_class = AddWorkerForm
    success_url = reverse_lazy("users:worker-list")
    template_name = "users/worker_form.html"
    crumbs = [
        ("", "Home"),
        ("My CoWorkers", reverse_lazy("users:worker-list")),
        ("Add new Worker", "")
    ]

    def test_func(self):
        return self.request.user.role == "Supervisor"

    def get_context_data(self, **kwargs):
        context = super(AddWorkerView, self).get_context_data(**kwargs)
        context["referer"] = self.request.META.get("HTTP_REFERER")
        context["is_update"] = False
        return context


class WorkerDetailView(LoginRequiredMixin, BaseBreadcrumbMixin, DetailView):
    model = WorkerUser
    template_name = "registration/profile.html"
    crumbs = [
        ("", "Home"),
        ("My CoWorkers", reverse_lazy("users:worker-list")),
        ("Profile", "")
    ]

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        user = self.get_object()

        if user.id != self.request.user.id:
            context["display_position"] = user.position
            if user.first_name and user.last_name:
                context["display_name"] = f"{user.first_name} {user.last_name}"
            else:
                context["display_name"] = user.username
        else:
            context["display_position"] = self.request.user.position
            if self.request.user.first_name and self.request.user.last_name:
                context["display_name"] = (
                    f"{self.request.user.first_name} "
                    f"{self.request.user.last_name}"
                )
            else:
                context["display_name"] = self.request.user.username

        return context


class WorkerUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    BaseBreadcrumbMixin,
    UpdateView
):
    model = WorkerUser
    form_class = WorkerUserUpdateForm
    template_name = "users/worker_form.html"

    crumbs = [
        ("", "Home"),
        ("My CoWorkers", reverse_lazy("users:worker-list")),
        ("Profile", ""),
        ("Edit", "")
    ]

    def test_func(self):
        return (
                self.get_object().id == self.request.user.id
                or self.request.user.role == "Supervisor"
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_role"] = self.request.user.role

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(WorkerUpdateView, self).get_context_data(**kwargs)
        next_url = self.request.GET.get("next")
        if next_url:
            context["referer"] = next_url
        context["is_update"] = True
        return context

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy(
            "users:worker-detail", kwargs={"pk": self.object.id}
        )


class WorkerListView(LoginRequiredMixin, BaseBreadcrumbMixin, ListView):
    model = WorkerUser
    template_name = "users/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 10

    crumbs = [("", "Home"), ("My CoWorkers", ""),]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        context["total_workers"] = WorkerUser.objects.all().count()
        title = self.request.GET.get("title", "")
        context["search_form"] = WorkerSearchForm(initial={"title": title})

        return context

    def get_queryset(self):
        queryset = WorkerUser.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data["title"]
            search_conditions = (
                    Q(username__icontains=search_term)
                    | Q(first_name__icontains=search_term)
                    | Q(last_name__icontains=search_term)
            )
            return queryset.filter(search_conditions)

        return queryset
