from django.db import models

# Create your models here.


class SlackMessage(models.Model):
    user_id = models.IntegerField()
    effect = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
