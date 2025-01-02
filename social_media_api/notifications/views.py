from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    data = [
        {
            "actor": notification.actor.username,
            "verb": notification.verb,
            "target": str(notification.target),
            "created_at": notification.created_at,
            "is_read": notification.is_read
        }
        for notification in notifications
    ]
    return Response(data)
