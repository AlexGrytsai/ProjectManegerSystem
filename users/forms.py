from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import WorkerUser
from users.models import Role


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WorkerUser
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
        )


class AddWorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WorkerUser
        fields = UserCreationForm.Meta.fields + ("role",
                                                 "position",
                                                 "is_active",
                                                 )


class WorkerUserUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = WorkerUser

        fields = ("username",
                  "email",
                  "first_name",
                  "last_name",
                  "role",
                  "position",
                  "is_active",
                  "phone_number",
                  "telegram",
                  "photo",
                  )

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop("user_role")
        super().__init__(*args, **kwargs)

        if user_role == Role.ENGINEER_MANAGER:
            self.fields.pop("position")
            self.fields.pop("role")
            self.fields.pop("is_active")
