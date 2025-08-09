from django.db import models

# Create your models here.


class WeeklyReport(models.Model):
    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, related_name='weekly_reports')
    department = models.ForeignKey('organizations.Department', on_delete=models.CASCADE, related_name='weekly_reports', null=True, blank=True)
    week_start = models.DateField()
    week_end = models.DateField()
    total_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)
    completed_on_time = models.PositiveIntegerField(default=0)
    quality_issues = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('organization', 'department', 'week_start', 'week_end')
        ordering = ['-week_start']

    @property
    def wnd_percent(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return round(100.0 * (self.total_tasks - self.completed_tasks) / self.total_tasks, 2)

    @property
    def wndot_percent(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return round(100.0 * (self.completed_tasks - self.completed_on_time) / self.total_tasks, 2)

    @property
    def quality_issue_percent(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return round(100.0 * self.quality_issues / self.total_tasks, 2)
