from .models import Message


def notifications(request):
    if not request.user.is_authenticated:
        return {
            "unread_notifications": [],
            "unread_notifications_count": 0,
        }

    unread_messages = (
        Message.objects
        .filter(
            receiver=request.user,
            is_read=False,
        )
        .select_related("sender")
        .order_by("-created_at")[:10]
    )

    unread_count = Message.objects.filter(
        receiver=request.user,
        is_read=False,
    ).count()

    return {
        "unread_notifications": unread_messages,
        "unread_notifications_count": unread_count,
    }