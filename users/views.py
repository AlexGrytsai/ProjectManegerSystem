from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from .forms import RegisterForm
from .forms import WorkerUserUpdateForm
from .models import WorkerUser


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"


class RegisterView(CreateView):
    model = WorkerUser
    form_class = RegisterForm
    template_name = "registration/register_form.html"

    success_url = reverse_lazy("users:login")


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = WorkerUser
    template_name = "registration/profile.html"

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
                context["display_name"] = (f"{self.request.user.first_name} "
                                           f"{self.request.user.last_name}")
            else:
                context["display_name"] = self.request.user.username

        return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkerUser
    form_class = WorkerUserUpdateForm
    template_name = "users/worker_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_role"] = self.request.user.role
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(WorkerUpdateView, self).get_context_data(**kwargs)
        context["previous_page"] = self.request.META.get("HTTP_REFERER")
        return context

    def get_success_url(self):
        return reverse_lazy(
            "users:worker-detail", kwargs={"pk": self.object.id}
        )
