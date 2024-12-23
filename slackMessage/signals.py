from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from slackMessage.views import send_slack_message
from .models import SlackMessage
from users.models import User


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    effect = "User Created" if created else "User Updated"
    message = f"User '{instance.id}' was {effect.lower()}."
    send_slack_message(instance.id, effect, message)
    SlackMessage.objects.create(user_id=instance.id, effect=effect, message=message)


# @receiver(m2m_changed, sender=User.permissions.through)
# def user_permissions_changed(sender, instance, action, **kwargs):
#     if action in ["post_add", "post_remove"]:
#         effect = "Permissions Changed"
#         message = f"Permissions for user '{instance.username}' were updated."
#         send_slack_message(instance.id, effect, message)
#         SlackMessage.objects.create(user_id=instance.id, effect=effect, message=message)
