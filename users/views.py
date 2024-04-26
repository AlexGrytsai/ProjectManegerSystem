from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class ProfileView(TemplateView):
    template_name = "registration/profile.html"
