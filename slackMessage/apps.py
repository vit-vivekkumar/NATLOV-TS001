from django.apps import AppConfig


class SlackmessageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "slackMessage"

    def ready(self):
        import slackMessage.signals
