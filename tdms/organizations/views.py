from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Department, DelegationMatrix
from .serializers import DepartmentSerializer, DelegationMatrixSerializer


class IsOrgAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [request.user.Role.ORG_ADMIN, request.user.Role.SUPER_ADMIN]


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.filter(organization=self.request.user.organization)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrgAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class DelegationMatrixViewSet(viewsets.ModelViewSet):
    serializer_class = DelegationMatrixSerializer

    def get_queryset(self):
        return DelegationMatrix.objects.filter(organization=self.request.user.organization)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrgAdmin()]
        return [permissions.IsAuthenticated()]
