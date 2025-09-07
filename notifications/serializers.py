from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserProfileSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = (
            'id', 'sender', 'notification_type', 'title', 'message',
            'action_data', 'is_read', 'created_at', 'read_at'
        )
        read_only_fields = (
            'id', 'sender', 'notification_type', 'title', 'message',
            'action_data', 'created_at', 'read_at'
        )
