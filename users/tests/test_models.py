from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase


class WorkerUserModelTest(TestCase):
    def setUp(self):
        self.mock_photo = MagicMock(spec=ImageFieldFile)
        self.mock_photo.size = 1024
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@example.com",
            password="password123",
            role="Supervisor",
            position="Developer",
            phone_number="+1234567890",
            telegram="@test_user",
            is_active=True,
            is_supervisor=True,
        )

    def test_str_method(self):
        self.assertEqual(str(self.user), f"{self.user.username}")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            f"/accounts/profile/{self.user.pk}/"
        )

    def test_clean_method_valid_phone_number(self):
        self.user.phone_number = "+3456789123"
        self.user.clean()

    def test_clean_method_invalid_phone_number(self):
        self.user.phone_number = "123456"
        with self.assertRaises(ValidationError):
            self.user.clean()

    def test_clean_method_valid_telegram(self):
        self.user.phone_number = None
        self.user.telegram = "@test"
        self.user.clean()

    def test_clean_method_invalid_telegram(self):
        self.user.telegram = "test"
        with self.assertRaises(ValidationError):
            self.user.clean()

    def test_clean_method_invalid_photo_size(self):
        with self.assertRaises(ValidationError):
            self.user.clean()

    def test_clean_method_valid_photo(self):
        self.user.phone_number = None
        self.user.photo = self.mock_photo
        self.assertEqual(self.user.photo, self.mock_photo)

        try:
            self.user.clean()
        except ValidationError:
            self.fail("Validation error raised unexpectedly")

        max_photo_size = 2097152  # 2 MB
        self.assertLessEqual(
            self.user.photo.size, max_photo_size, "Photo size should be within limits"
        )

    def test_clean_method_invalid_photo(self):
        self.mock_photo.size = 5024

        with self.assertRaises(ValidationError):
            self.user.clean()
