from django.http import HttpResponseForbidden
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from users.models import WorkerUser

WORKERS_LIST_URL = [
    reverse("users:index"),
    reverse("users:worker-list"),
    reverse("users:worker-detail", kwargs={"pk": 1}),
    reverse("users:worker-update", kwargs={"pk": 1}),
]


class PublicViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        for url in WORKERS_LIST_URL:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)

    def test_access_to_login_page(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_access_to_register_page(self):
        response = self.client.get(reverse("users:register-user"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register_form.html")


class WorkerLoggedInViewsTest(TestCase):

    def setUp(self):
        self.worker = WorkerUser.objects.create(
            username="test_user",
            email="test@example.com",
            role="Supervisor",
            position="Developer",
            is_active=True,
            is_supervisor=True,
        )

        self.worker2 = WorkerUser.objects.create(
            username="test_user2",
            email="test@example.com",
            role="Guest",
            position="Developer",
            is_active=True,
            is_supervisor=True,
        )

        self.client.force_login(self.worker)

    def test_retrieve_all_pages(self):
        for url in WORKERS_LIST_URL:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def test_validate_add_new_worker(self):
        response = self.client.get(reverse("users:add-worker"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/worker_form.html")

    def test_invalidate_add_new_worker(self):
        self.worker.role = "Guest"
        self.worker.save()
        response = self.client.get(reverse("users:add-worker"))

        self.assertEqual(response.status_code, 403)
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_validate_update_worker(self):
        response = self.client.get(
            reverse("users:worker-update", kwargs={"pk": self.worker2.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/worker_form.html")

        self.client.force_login(self.worker2)

        response = self.client.get(
            reverse("users:worker-update", kwargs={"pk": self.worker.id})
        )

        self.assertEqual(response.status_code, 403)

        response = self.client.get(
            reverse("users:worker-update", kwargs={"pk": self.worker2.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_invalidate_update_worker(self):
        self.client.force_login(self.worker2)
        response = self.client.get(
            reverse("users:worker-update", kwargs={"pk": self.worker.id})
        )

        self.assertEqual(response.status_code, 403)
