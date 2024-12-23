import logging
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from slackMessage.models import SlackMessage
from students.models import Student
from .models import User
from slackMessage.views import send_slack_message

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Automatically create a Student profile when a new User is created."""
    if created:
        Student.objects.create(user=instance, name=instance.first_name)
        message = f"New student profile created for User: {instance.first_name} {instance.last_name} (ID: {instance.id})"
        send_slack_message(
            user_id=instance.id, effect="Profile Creation", message=message
        )
        print(message)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login events."""
    ip_address = request.META.get("REMOTE_ADDR", "Unknown IP")
    message = f"User {user.first_name} {user.last_name} (ID: {user.id}) logged in from IP: {ip_address}"
    send_slack_message(user_id=user.id, effect="Login", message=message)
    print(message)


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout events."""
    ip_address = request.META.get("REMOTE_ADDR", "Unknown IP")
    message = f"User {user.first_name} {user.last_name} (ID: {user.id}) logged out from IP: {ip_address}"
    send_slack_message(user_id=user.id, effect="Logout", message=message)
    print(message)


@receiver(m2m_changed, sender=User.user_permissions.through)
def user_permissions_changed(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove"]:
        effect = "Permissions Changed"
        message = f"Permissions for user '{instance.email}' were updated."
        send_slack_message(instance.id, effect, message)
        SlackMessage.objects.create(user_id=instance.id, effect=effect, message=message)
