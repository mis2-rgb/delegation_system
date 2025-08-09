from django.db import models
from django.conf import settings


class Notification(models.Model):
    class Type(models.TextChoices):
        NEW_TASK = 'new_task', 'New Task'
        TASK_COMPLETED = 'task_completed', 'Task Completed'
        QUALITY_ISSUE = 'quality_issue', 'Quality Issue'
        TASK_REGENERATED = 'task_regenerated', 'Task Regenerated'

    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, related_name='notifications')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=32, choices=Type.choices)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    related_task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'to_user', 'is_read']),
            models.Index(fields=['organization', 'created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.notification_type}: {self.title}"
