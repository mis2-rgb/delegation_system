from django.urls import path
from .views import DashboardMetricsView, WeeklyReportListView

urlpatterns = [
    path('weekly/', WeeklyReportListView.as_view(), name='weekly-reports'),
    path('metrics/', DashboardMetricsView.as_view(), name='dashboard-metrics'),
]