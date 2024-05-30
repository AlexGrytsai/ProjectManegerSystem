from django.http import HttpResponseRedirect
from django.test import TestCase, RequestFactory
from django.urls import reverse

from projects.forms import ProjectCreateForm
from projects.models import Project
from projects.views import ProjectCreateView
from users.models import WorkerUser


class ProjectCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.supervisor = WorkerUser.objects.create_user(
            username="supervisor",
            password="testpassword",
            role="Supervisor"
        )
        self.non_supervisor = WorkerUser.objects.create_user(
            username="nonsupervisor",
            password="testpassword",
            role="Guest"
        )

    def test_get_form_class(self) -> None:
        view = ProjectCreateView()
        self.assertEqual(view.get_form_class(), ProjectCreateForm)

    def test_access_for_supervisor(self) -> None:
        request = self.factory.get(reverse("projects:create-project"))
        request.user = self.supervisor

        view = ProjectCreateView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_no_access_for_non_supervisor(self) -> None:
        self.client.force_login(self.non_supervisor)

        response = self.client.get(reverse("projects:create-project"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_form_valid_adds_user_to_responsible_workers(self):
        data = {
            "name": "Test Project",
            "description": "A test project description",
            "status": "Developing",
        }

        request = self.factory.post(reverse("projects:create-project"))
        request.user = self.supervisor

        view = ProjectCreateView()
        view.request = request

        form = ProjectCreateForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors)

        view.object = form.save(commit=False)
        view.object.project_lead = self.supervisor

        response = view.form_valid(form)
        self.assertEqual(response.status_code, 302)

        project = Project.objects.get(name="Test Project",
                                      project_lead=self.supervisor)
        self.assertIn(self.supervisor, project.responsible_workers.all())

    def test_get_context_data(self) -> None:
        request = self.factory.get(reverse("projects:create-project"))
        request.user = self.supervisor

        view = ProjectCreateView()
        view.request = request
        view.object = None

        context = view.get_context_data()

        self.assertIn("is_update", context)
        self.assertTrue(context["is_update"])

    def test_get_success_url(self) -> None:
        request = self.factory.get(reverse("projects:create-project"))
        request.user = self.supervisor

        view = ProjectCreateView()
        view.request = request

        success_url = view.get_success_url()
        self.assertEqual(success_url, "/")
