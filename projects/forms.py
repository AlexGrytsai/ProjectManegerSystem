from django import forms
from django.db.models import Q

from users.models import WorkerUser
from .models import Project


class ProjectCreateForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        required=False
    )

    conditions = Q(is_active=True) & Q(role="Engineer/Manager")
    responsible_workers = forms.ModelMultipleChoiceField(
        queryset=WorkerUser.objects.filter(conditions).order_by("position"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = (
            "name",
            "description",
            "deadline",
            "project_lead",
            "responsible_workers"
        )
