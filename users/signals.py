from django.db.models.signals import pre_migrate
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_migrate)
def create_groups_and_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from .models import Role
    for role in Role:
        group, created = Group.objects.get_or_create(name=role.label)
        if created:
            add_user = Permission.objects.get(codename="users.add_user")
            change_user = Permission.objects.get(codename="users.change_user")
            activate_user = Permission.objects.get(
                codename="users.activate_user"
            )
            view_user = Permission.objects.get(codename="users.view_user")

            if role == Role.GUEST:
                guest_permissions = [view_user, ]
                group.permissions.add(*guest_permissions)
            elif role == Role.ENGINEER_MANAGER:
                engineer_manager_permissions = [
                    view_user,
                ]
                group.permissions.add(*engineer_manager_permissions)
            elif role == Role.SUPERVISOR:
                supervisor_permissions = [
                    view_user, add_user, change_user, activate_user,
                ]
                group.permissions.add(*supervisor_permissions)


@receiver(pre_save, sender="users.WorkerUser")
def update_user_in_group(sender, instance, **kwargs):
    from .models import WorkerUser
    try:
        old_role = WorkerUser.objects.get(pk=instance.pk).role
    except WorkerUser.DoesNotExist:
        old_role = None

    new_role = instance.role

    if old_role != new_role:
        from django.contrib.auth.models import Group
        old_group = Group.objects.get(name=old_role)
        new_group = Group.objects.get(name=new_role)

        if old_group and old_group in instance.groups.all():
            instance.groups.remove(old_group)

        if new_group:
            instance.groups.add(new_group)
