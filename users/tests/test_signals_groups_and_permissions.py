from django.contrib.auth.models import Group
from django.test import TestCase

from users.models import Role
from users.signals import create_groups_and_permissions


class TestSignalHandlers(TestCase):
    def test_create_groups_and_permissions(self):
        create_groups_and_permissions(sender=self.__class__)

        self.assertEqual(Group.objects.count(), len(Role.choices))

        for role in Role.choices:
            group_name = role[1]
            group = Group.objects.get(name=group_name)
            permissions = group.permissions.all()
            self.assertTrue(permissions.exists())

            if group_name == 'Guest':
                expected_permissions = [
                    'users.change_user',
                    'users.view_user',
                ]
            elif group_name == 'Engineer/Manager':
                expected_permissions = [
                    'users.change_user',
                    'users.view_user',
                ]
            elif group_name == 'Supervisor':
                expected_permissions = [
                    'users.add_user',
                    'users.change_user',
                    'users.change_another_user',
                    'users.activate_user',
                    'users.view_user',
                ]
            else:
                expected_permissions = []

            for codename in expected_permissions:
                self.assertTrue(permissions.filter(codename=codename).exists())
