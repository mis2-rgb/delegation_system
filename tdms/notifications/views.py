from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


# Create your views here.


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(organization=self.request.user.organization, to_user=self.request.user)


class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user:
            return Response({'detail': 'Forbidden'}, status=403)
        instance.is_read = True
        instance.save()
        return Response(NotificationSerializer(instance).data)
