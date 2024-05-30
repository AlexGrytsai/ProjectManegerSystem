from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import WorkerUser


@admin.register(WorkerUser)
class WorkerUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "is_active",
        "position",
        "role",
        "phone_number",
        "telegram",
        "is_supervisor",
    )

    details_info = (
        "Details info",
        {
            "fields": (
                "position",
                "role",
                "phone_number",
                "telegram",
                "photo",
            )
        },
    )

    permissions = (
        "Permissions",
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_supervisor",
                "is_superuser",
                "user_permissions",
            )
        },
    )

    fieldsets = (
        UserAdmin.fieldsets[0],
        UserAdmin.fieldsets[1],
        details_info,
        permissions,
        UserAdmin.fieldsets[3],
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "position",
                    "role",
                    "is_supervisor",
                    "phone_number",
                    "telegram",
                    "photo",
                )
            },
        ),
    )

    list_filter = ["position", "role", "is_supervisor"]
