from celery import shared_task
from django.utils import timezone
from .models import Task
from notifications.utils import notify_user


@shared_task
def regenerate_incomplete_tasks():
    now = timezone.now()
    # Incomplete = active tasks without completion and past Saturday 5 PM cutoff
    tasks = Task.objects.filter(is_active=True, completion__isnull=True, complete_by__lt=now)
    for task in tasks:
        task.regenerated_count += 1
        # Extend to next week same deadline time
        task.complete_by = task.complete_by + timezone.timedelta(days=7)
        task.save(update_fields=['regenerated_count', 'complete_by'])
        notify_user(task.doer, 'task_regenerated', f'Task {task.delegation_id} regenerated', task)