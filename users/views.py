from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import DetailView

from .forms import RegisterForm
from .models import WorkerUser


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"


class RegisterView(CreateView):
    model = WorkerUser
    form_class = RegisterForm
    template_name = "registration/register_form.html"

    success_url = reverse_lazy("users:login")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = WorkerUser
    template_name = "registration/profile.html"
