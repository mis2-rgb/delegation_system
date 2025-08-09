from django.contrib import admin
from .models import Task, TaskCompletion


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("delegation_id", "organization", "department", "doer", "priority", "complete_by", "regenerated_count")
    list_filter = ("organization", "department", "priority")
    search_fields = ("delegation_id", "description")


@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
    list_display = ("task", "completed_by", "completed_at", "is_accepted", "quality_issue")
    list_filter = ("quality_issue",)
