from django.contrib import admin
from .models import Department, DelegationMatrix


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")
    list_filter = ("organization",)
    search_fields = ("name",)


@admin.register(DelegationMatrix)
class DelegationMatrixAdmin(admin.ModelAdmin):
    list_display = ("organization", "department", "delegator", "doer")
    list_filter = ("organization", "department")
