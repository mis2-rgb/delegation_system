from django.db import models
from django.conf import settings


class Department(models.Model):
    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name} ({self.organization})"


class DelegationMatrix(models.Model):
    organization = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, related_name='delegation_matrices')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='delegation_rules')
    delegator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_delegate_rules')
    doer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_do_rules')

    class Meta:
        unique_together = ('organization', 'department', 'delegator', 'doer')

    def __str__(self) -> str:
        return f"{self.delegator} -> {self.doer} [{self.department}]"
