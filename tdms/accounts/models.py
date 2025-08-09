from django.contrib.auth.models import AbstractUser
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        ORG_ADMIN = "org_admin", "Organization Admin"
        HOD = "hod", "HOD"
        EA = "ea", "EA"
        DOER = "doer", "Doer"
        DELEGATOR = "delegator", "Delegator"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.DOER)
    department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True)

    def is_super_admin(self) -> bool:
        return self.role == self.Role.SUPER_ADMIN

    def is_org_admin(self) -> bool:
        return self.role == self.Role.ORG_ADMIN

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
