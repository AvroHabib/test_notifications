import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from django.utils import timezone
from celery import shared_task
from pathlib import Path
from .models import Notification, NotificationDelivery
from accounts.models import User, UserDevice
from posts.models import Post, Comment
import logging

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    if settings.FIREBASE_CREDENTIALS_PATH and Path(settings.FIREBASE_CREDENTIALS_PATH).exists():
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Firebase: {e}")
    else:
        logger.warning("Firebase credentials not configured or file not found")


@shared_task
def send_post_notification(post_id):
    """Send notification to all users when a new post is created"""
    try:
        post = Post.objects.get(id=post_id)
        
        # Get all users except the post author
        recipients = User.objects.filter(is_active=True).exclude(id=post.author.id)
        
        for recipient in recipients:
            # Create notification record
            notification = Notification.objects.create(
                recipient=recipient,
                sender=post.author,
                notification_type='new_post',
                title='New Post',
                message=f"{post.author.get_full_name()} posted something new",
                post=post,
                action_data={
                    'type': 'new_post',
                    'post_id': post.id,
                    'navigate_to': 'post_detail'
                }
            )
            
            # Send to all active devices
            send_notification_to_user.delay(notification.id, recipient.id)
            
    except Post.DoesNotExist:
        logger.error(f"Post {post_id} not found")
    except Exception as e:
        logger.error(f"Error sending post notification: {str(e)}")


@shared_task
def send_comment_notification(comment_id):
    """Send notification to post author when someone comments"""
    try:
        comment = Comment.objects.get(id=comment_id)
        post_author = comment.post.author
        
        # Don't send notification if user comments on their own post
        if comment.author == post_author:
            return
        
        # Create notification record
        notification = Notification.objects.create(
            recipient=post_author,
            sender=comment.author,
            notification_type='new_comment',
            title='New Comment',
            message=f"{comment.author.get_full_name()} commented on your post",
            post=comment.post,
            comment=comment,
            action_data={
                'type': 'new_comment',
                'post_id': comment.post.id,
                'comment_id': comment.id,
                'navigate_to': 'comment_detail'
            }
        )
        
        # Send to all active devices
        send_notification_to_user.delay(notification.id, post_author.id)
        
    except Comment.DoesNotExist:
        logger.error(f"Comment {comment_id} not found")
    except Exception as e:
        logger.error(f"Error sending comment notification: {str(e)}")


@shared_task
def send_notification_to_user(notification_id, user_id):
    """Send FCM notification to all active devices of a user"""
    try:
        notification = Notification.objects.get(id=notification_id)
        user = User.objects.get(id=user_id)
        
        # Get all active devices for the user
        devices = UserDevice.objects.filter(user=user, is_active=True)
        
        if not devices.exists():
            logger.info(f"No active devices found for user {user.phone_number}")
            return
        
        # Prepare FCM message
        fcm_message_data = {
            'title': notification.title,
            'body': notification.message,
            'data': {
                'notification_id': str(notification.id),
                'type': notification.notification_type,
                'action_data': str(notification.action_data)
            }
        }
        
        successful_deliveries = 0
        
        for device in devices:
            try:
                # Create delivery record
                delivery, created = NotificationDelivery.objects.get_or_create(
                    notification=notification,
                    device=device
                )
                
                if not created and delivery.is_delivered:
                    continue  # Already delivered
                
                # Send FCM message
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=fcm_message_data['title'],
                        body=fcm_message_data['body']
                    ),
                    data=fcm_message_data['data'],
                    token=device.fcm_token
                )
                
                response = messaging.send(message)
                
                # Update delivery status
                delivery.is_delivered = True
                delivery.delivered_at = timezone.now()
                delivery.save()
                
                successful_deliveries += 1
                logger.info(f"Notification sent successfully to {device.fcm_token}: {response}")
                
            except messaging.UnregisteredError:
                # Token is invalid, deactivate device
                device.is_active = False
                device.save()
                delivery.error_message = "Invalid FCM token"
                delivery.save()
                logger.warning(f"Invalid FCM token for device {device.id}, deactivated")
                
            except Exception as e:
                delivery.error_message = str(e)
                delivery.save()
                logger.error(f"Error sending notification to device {device.id}: {str(e)}")
        
        # Update notification status
        if successful_deliveries > 0:
            notification.is_sent = True
            notification.save()
            
    except (Notification.DoesNotExist, User.DoesNotExist) as e:
        logger.error(f"Notification or User not found: {str(e)}")
    except Exception as e:
        logger.error(f"Error in send_notification_to_user: {str(e)}")
