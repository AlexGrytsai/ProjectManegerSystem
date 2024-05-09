from django.test import TestCase
from users.models import WorkerUser, Role, Position
from users.forms import (
    RegisterForm,
    AddWorkerForm,
    WorkerUserUpdateForm,
    WorkerSearchForm,
)


class TestForms(TestCase):
    def setUp(self):
        WorkerUser.objects.create(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=Role.ENGINEER_MANAGER,
            position=Position.DEVOPS,
            is_active=True,
        )

        WorkerUser.objects.create(
            username="testuser2",
            email="test2@example.com",
            first_name="Test2",
            last_name="User2",
            role=Role.SUPERVISOR,
            position=Position.DEVELOPER,
            is_active=True,
        )

    def test_register_form(self):
        data = {
            "username": "testuser3",
            "password1": "!123456789",
            "password2": "!123456789",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }
        form = RegisterForm(data)
        self.assertTrue(form.is_valid())

    def test_add_worker_form(self):
        data = {
            "username": "testuser3",
            "password1": "testpassword",
            "password2": "testpassword",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "Guest",
            "position": "Guest",
            "is_active": True,
        }
        form = AddWorkerForm(data)
        self.assertTrue(form.is_valid())

    def test_worker_user_update_form(self):
        data = {
            "username": "testuser3",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "Supervisor",
            "position": "Developer",
            "is_active": True,
            "phone_number": "+3456789123",
            "telegram": "@testuser",
        }
        form = WorkerUserUpdateForm(data, user_role=Role.ENGINEER_MANAGER)
        self.assertTrue(form.is_valid())

    def test_worker_search_form(self):
        data = {"title": "Test Title"}
        form = WorkerSearchForm(data)
        self.assertTrue(form.is_valid())
