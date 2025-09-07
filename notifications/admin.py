from django.contrib import admin
from .models import Notification, NotificationDelivery


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'sender', 'notification_type', 'title', 'is_read', 'is_sent', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_sent', 'created_at')
    search_fields = ('recipient__phone_number', 'sender__phone_number', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')
    list_per_page = 20


@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'device', 'is_delivered', 'delivered_at', 'created_at')
    list_filter = ('is_delivered', 'delivered_at', 'created_at')
    search_fields = ('notification__title', 'device__user__phone_number')
    readonly_fields = ('created_at', 'delivered_at')
    list_per_page = 20
