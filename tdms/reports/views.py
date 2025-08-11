from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Count, Q, F
from django.utils import timezone
from datetime import timedelta

from tasks.models import Task, TaskCompletion
from .models import WeeklyReport
from .serializers import WeeklyReportSerializer


# Create your views here.


class DashboardMetricsView(generics.GenericAPIView):
    def get(self, request):
        org = request.user.organization
        qs = Task.objects.filter(organization=org)
        total = qs.count()
        completed = TaskCompletion.objects.filter(task__organization=org).count()
        quality_issues = TaskCompletion.objects.filter(task__organization=org, quality_issue=True).count()
        on_time = TaskCompletion.objects.filter(task__organization=org, task__complete_by__gte=F('completed_at')).count() if completed else 0
        data = {
            'total_tasks': total,
            'completed_tasks': completed,
            'quality_issues': quality_issues,
            'completion_rate': round(100.0 * completed / total, 2) if total else 0.0,
            'wnd_percent': round(100.0 * (total - completed) / total, 2) if total else 0.0,
            'wndot_percent': round(100.0 * (completed - on_time) / total, 2) if total else 0.0,
        }
        return Response(data)


class WeeklyReportListView(generics.ListAPIView):
    serializer_class = WeeklyReportSerializer

    def get_queryset(self):
        return WeeklyReport.objects.filter(organization=self.request.user.organization)
