from django.db import models
from django.conf import settings


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'

    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, related_name='tasks')
    delegation_id = models.CharField(max_length=32, unique=True)
    delegator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delegated_tasks')
    department = models.ForeignKey('organizations.Department', on_delete=models.CASCADE, related_name='tasks')
    doer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tasks')
    description = models.TextField()
    complete_by = models.DateTimeField()
    priority = models.CharField(max_length=16, choices=Priority.choices, default=Priority.MEDIUM)
    attachment_image = models.ImageField(upload_to='attachments/images/', null=True, blank=True)
    attachment_file = models.FileField(upload_to='attachments/files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    regenerated_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'delegation_id']),
            models.Index(fields=['organization', 'doer', 'complete_by']),
            models.Index(fields=['organization', 'department']),
        ]
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.delegation_id}: {self.description[:30]}"


class TaskCompletion(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='completion')
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_completions')
    completed_at = models.DateTimeField(auto_now_add=True)
    proof_image = models.ImageField(upload_to='proof/images/', null=True, blank=True)
    proof_file = models.FileField(upload_to='proof/files/', null=True, blank=True)
    remarks = models.TextField(blank=True)
    quality_issue = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_tasks')
    verified_at = models.DateTimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Completion of {self.task.delegation_id}"
