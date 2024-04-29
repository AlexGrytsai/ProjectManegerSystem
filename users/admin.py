from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Worker
from .models import Supervisor


@admin.register(Supervisor)
class SupervisorAdmin(UserAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass
