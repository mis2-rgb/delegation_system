from rest_framework import serializers
from .models import WeeklyReport


class WeeklyReportSerializer(serializers.ModelSerializer):
    wnd_percent = serializers.FloatField(read_only=True)
    wndot_percent = serializers.FloatField(read_only=True)
    quality_issue_percent = serializers.FloatField(read_only=True)

    class Meta:
        model = WeeklyReport
        fields = ['id', 'department', 'week_start', 'week_end', 'total_tasks', 'completed_tasks', 'completed_on_time', 'quality_issues', 'wnd_percent', 'wndot_percent', 'quality_issue_percent']