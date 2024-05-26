from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender="projects.Comment")
def update_task_and_project_update_fild_after_update_comment(
        sender: "projects.Comment",
        instance: "projects.Comment",
        **kwargs
) -> None:
    if instance.pk:
        old_comment = sender.objects.get(pk=instance.pk)
        if old_comment.text != instance.text:
            related_task = instance.tasks.first()
            if related_task:
                related_task.save(update_fields=["updated"])

            related_project = related_task.project_tasks.first()
            if related_project:
                related_project.save(update_fields=["updated"])


@receiver(pre_delete, sender="projects.Comment")
def update_task_and_project_update_fild_after_delete_comment(
        instance: "projects.Comment",
        **kwargs
) -> None:
    related_task = instance.tasks.first()
    if related_task:
        related_task.save(update_fields=["updated"])

    related_project = related_task.project_tasks.first()
    if related_project:
        related_project.save(update_fields=["updated"])


@receiver(pre_delete, sender="projects.Task")
def update_project_update_fild_after_delete_task(
        instance: "projects.Task",
        **kwargs
) -> None:
    related_project = instance.project_tasks.first()
    if related_project:
        related_project.save(update_fields=["updated"])


@receiver(pre_save, sender="projects.Task")
def update_project_update_fild_after_update_task(
        sender: "projects.Task",
        instance: "projects.Task",
        **kwargs
) -> None:
    if instance.pk:
        print("task update")
        related_project = instance.project_tasks.first()
        if related_project:
            related_project.save(update_fields=["updated"])
