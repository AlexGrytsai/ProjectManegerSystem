from django.contrib.auth.forms import UserCreationForm

from users.models import WorkerUser


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WorkerUser
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
        )
