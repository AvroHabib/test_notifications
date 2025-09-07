from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationListView,
    mark_notification_read,
    mark_all_notifications_read,
    unread_notification_count
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread/', UnreadNotificationListView.as_view(), name='unread-notification-list'),
    path('count/', unread_notification_count, name='unread-notification-count'),
    path('<int:notification_id>/read/', mark_notification_read, name='mark-notification-read'),
    path('mark-all-read/', mark_all_notifications_read, name='mark-all-notifications-read'),
]
