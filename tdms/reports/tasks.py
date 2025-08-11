from celery import shared_task
from django.utils import timezone
from django.db.models import Count, Q, F
from datetime import timedelta

from accounts.models import Organization
from tasks.models import Task, TaskCompletion
from .models import WeeklyReport


def get_week_bounds(dt):
    # Week boundary Saturday 5 PM cutoff: week is from Sat 5:00 PM previous to Sat 4:59:59 PM current
    # We compute last Saturday 17:00 and the one before
    weekday = dt.weekday()  # Monday=0 ... Sunday=6
    # Find last Saturday 17:00
    days_since_saturday = (weekday - 5) % 7
    last_sat = (dt - timedelta(days=days_since_saturday)).replace(hour=17, minute=0, second=0, microsecond=0)
    prev_sat = last_sat - timedelta(days=7)
    return prev_sat.date(), last_sat.date()


@shared_task
def compute_weekly_reports():
    now = timezone.now()
    week_start, week_end = get_week_bounds(now)
    for org in Organization.objects.all():
        tasks = Task.objects.filter(organization=org, created_at__date__gte=week_start, created_at__date__lt=week_end)
        total = tasks.count()
        completions = TaskCompletion.objects.filter(task__in=tasks)
        completed = completions.count()
        quality_issues = completions.filter(quality_issue=True).count()
        on_time = completions.filter(task__complete_by__gte=F('completed_at')).count() if completed else 0
        report, _ = WeeklyReport.objects.get_or_create(
            organization=org,
            department=None,
            week_start=week_start,
            week_end=week_end,
            defaults={'total_tasks': total, 'completed_tasks': completed, 'completed_on_time': on_time, 'quality_issues': quality_issues}
        )
        if _ is False:
            report.total_tasks = total
            report.completed_tasks = completed
            report.completed_on_time = on_time
            report.quality_issues = quality_issues
            report.save()