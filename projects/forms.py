from django import forms
from django.db.models import Q

from users.models import WorkerUser
from .models import Project, Task


class ProjectCreateForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        required=False
    )
    conditions = Q(is_active=True) & Q(role="Engineer/Manager")
    project_lead = forms.ModelChoiceField(
        queryset=WorkerUser.objects.filter(role="Supervisor")
    )
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


class ProjectUpdateForm(forms.ModelForm):
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
            "status",
            "deadline",
            "project_lead",
            "responsible_workers"
        )


class TaskCreateForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        required=False
    )
    responsible_workers = forms.ModelMultipleChoiceField(
        queryset=WorkerUser.objects.none(),
        widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "type",
            "priority",
            "responsible_workers",
        )

    def __init__(self, project, *args, **kwargs) -> None:
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.fields["responsible_workers"].queryset = (
            project.responsible_workers.all()
        )


class TaskUpdateForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        required=False
    )

    responsible_workers = forms.ModelMultipleChoiceField(
        queryset=WorkerUser.objects.none(),
        widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "type",
            "priority",
            "status",
            "type",
            "priority",
            "responsible_workers",
        )
