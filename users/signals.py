from django.db.models.signals import post_save
from django.db.models.signals import pre_migrate
from django.db.models.signals import pre_save
from django.dispatch import receiver


def create_and_add_permissions_to_groups(group: "Group", **kwargs) -> None:
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    from .models import WorkerUser

    content_type_user = ContentType.objects.get_for_model(WorkerUser)

    permission_users_app_guest_group = [
        {
            "codename": "users.change_user",
            "name": "Can only change own account information",
            "content_type": content_type_user
        },
        {
            "codename": "users.view_user",
            "name": "View user",
            "content_type": content_type_user
        },
    ]

    permission_users_app_engineer_manager_group = [
        {
            "codename": "users.change_user",
            "name": "Can only change own account information",
            "content_type": content_type_user
        },
        {
            "codename": "users.view_user",
            "name": "View user",
            "content_type": content_type_user
        },
    ]

    permission_users_app_supervisor_group = [
        {
            "codename": "users.add_user",
            "name": "Add new worker",
            "content_type": content_type_user
        },
        {
            "codename": "users.change_user",
            "name": "Can only change own account information",
            "content_type": content_type_user
        },
        {
            "codename": "users.change_another_user",
            "name": "Can change another worker's account",
            "content_type": content_type_user
        },
        {
            "codename": "users.activate_user",
            "name": "Activate worker account",
            "content_type": content_type_user
        },
        {
            "codename": "users.view_user",
            "name": "View user",
            "content_type": content_type_user
        }
    ]

    group_name = group.name
    group_permissions_list = group.permissions.values_list(
        "codename", flat=True
    )

    if group_name == "Guest":
        for permission in permission_users_app_guest_group:
            if permission["codename"] not in group_permissions_list:
                new_permission, created = Permission.objects.get_or_create(
                    **permission
                )
                group.permissions.add(new_permission)

    if group_name == "Engineer/Manager":
        for permission in permission_users_app_engineer_manager_group:
            if permission["codename"] not in group_permissions_list:
                new_permission, created = Permission.objects.get_or_create(
                    **permission
                )
                group.permissions.add(new_permission)

    if group_name == "Supervisor":
        for permission in permission_users_app_supervisor_group:
            if permission["codename"] not in group_permissions_list:
                new_permission, created = Permission.objects.get_or_create(
                    **permission
                )
                group.permissions.add(new_permission)


@receiver(pre_migrate)
def create_groups_and_permissions(sender, **kwargs) -> None:
    from django.contrib.auth.models import Group
    from .models import Role

    for role in Role:
        group, created = Group.objects.get_or_create(name=role.label)

        if created:
            group.save()

    groups = Group.objects.all()

    for group in groups:
        create_and_add_permissions_to_groups(group)


@receiver(post_save, sender="users.WorkerUser")
def update_user_in_group(sender, instance, **kwargs) -> None:
    from django.contrib.auth.models import Group

    try:
        old_role = sender.objects.get(pk=instance.pk).role
    except sender.DoesNotExist:
        old_role = None

    try:
        old_group = Group.objects.get(name=old_role)
    except Group.DoesNotExist:
        old_group = None

    new_role = instance.role
    new_group = Group.objects.get(name=new_role)

    if old_role != new_role:

        if old_group and old_group in instance.groups.all():
            instance.groups.remove(old_group)

        if new_group:
            instance.groups.add(new_group)
    else:
        instance.groups.add(new_group)


@receiver(pre_save, sender="users.WorkerUser")
def delete_old_photo(sender, instance, **kwargs):
    from django.core.files.storage import default_storage
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.photo and old_instance.photo != instance.photo:
                path_to_old_photo = old_instance.photo.path
                default_storage.delete(path_to_old_photo)
        except sender.DoesNotExist:
            pass
