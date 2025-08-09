from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Task, TaskCompletion
from .serializers import TaskSerializer, TaskCompletionSerializer
from notifications.utils import notify_user


class IsHodOrDelegator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [request.user.Role.HOD, request.user.Role.DELEGATOR, request.user.Role.ORG_ADMIN, request.user.Role.SUPER_ADMIN]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_fields = ['department', 'doer', 'priority']
    search_fields = ['description', 'delegation_id']
    ordering_fields = ['created_at', 'complete_by']

    def get_queryset(self):
        return Task.objects.filter(organization=self.request.user.organization)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsHodOrDelegator()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.doer != request.user:
            return Response({'detail': 'Only assigned doer can complete this task.'}, status=403)
        serializer = TaskCompletionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)
        notify_user(task.delegator, 'task_completed', f'Task {task.delegation_id} completed', task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        task = self.get_object()
        if task.delegator != request.user and request.user.role not in [request.user.Role.EA, request.user.Role.ORG_ADMIN, request.user.Role.SUPER_ADMIN]:
            return Response({'detail': 'Only delegator/EA/admin can verify.'}, status=403)
        completion = task.completion
        accepted = request.data.get('accepted', True)
        quality_issue = not bool(accepted)
        completion.verified_by = request.user
        completion.verified_at = timezone.now()
        completion.is_accepted = bool(accepted)
        completion.quality_issue = bool(quality_issue)
        completion.save()
        if quality_issue:
            notify_user(task.doer, 'quality_issue', f'Quality issue on task {task.delegation_id}', task)
        return Response(TaskCompletionSerializer(completion).data)
