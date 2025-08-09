from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification


def notify_user(user, notification_type: str, title: str, task=None, message: str = ""):
    notification = Notification.objects.create(
        organization=user.organization,
        to_user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_task=task,
    )
    channel_layer = get_channel_layer()
    group = f"org_{user.organization_id}_user_{user.id}_notifications"
    async_to_sync(channel_layer.group_send)(group, {
        'type': 'notify',
        'data': {
            'id': notification.id,
            'type': notification.notification_type,
            'title': notification.title,
            'message': notification.message,
            'task_id': notification.related_task_id,
            'created_at': notification.created_at.isoformat(),
        }
    })
    return notification