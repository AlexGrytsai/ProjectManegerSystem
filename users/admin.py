from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import WorkerUser


@admin.register(WorkerUser)
class WorkerUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "is_active",
        "title",
        "role",
        "phone_number",
        "telegram",
        "is_supervisor",
    )

    details_info = (
        "Details info", {
            "fields": (
                "title",
                "role",
                "phone_number",
                "telegram",
                "photo",
            )
        }
    )

    permissions = (
        "Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_supervisor",
                "is_superuser",
                "user_permissions",
            )
        }
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
            "Additional info", {
                "fields": (
                    "title",
                    "role",
                    "is_supervisor",
                    "phone_number",
                    "telegram",
                    "photo",
                )
            }
        ),
    )

    list_filter = ["title", "role", "is_supervisor"]
