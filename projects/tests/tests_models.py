from django.contrib.auth import get_user_model
from django.test import TestCase

from projects.models import Comment
from projects.models import Project
from projects.models import ProjectStatus
from projects.models import TackStatus
from projects.models import Task
from projects.models import TaskPriority
from projects.models import TaskType
from users.models import WorkerUser


class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = WorkerUser.objects.create_user(
            username="test_user",
            email="test@example.com",
            is_active=True,
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Test description",
            project_lead=self.user,
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.project),
            f"{self.project.name} by {self.project.project_lead}"
        )

    def test_project_default_status(self):
        self.assertEqual(self.project.status, ProjectStatus.DEVELOPING)


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = WorkerUser.objects.create_user(
            username="test_user",
            email="test@example.com",
            is_active=True,
        )
        self.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            author=self.user,
        )

    def test_str_method(self):
        self.assertEqual(str(self.task), f"{self.task.name}")

    def test_task_default_status(self):
        self.assertEqual(self.task.status, TackStatus.CREATED)

    def test_task_default_type(self):
        self.assertEqual(self.task.type, TaskType.INDEFINITE)

    def test_task_default_priority(self):
        self.assertEqual(self.task.priority, TaskPriority.LOW)


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

    def test_str_method(self):
        comment = Comment.objects.create(text="Test comment", author=self.user)
        expected_str = (
            f"{comment.text}\nAuthor: {comment.author}\nCreated: "
            f"{comment.created}"
        )
        self.assertEqual(str(comment), expected_str)
