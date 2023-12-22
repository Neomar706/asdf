from django.db import models
from django.utils import timezone


class History(models.Model):
    channel    = models.ForeignKey('channel.Channel', on_delete=models.CASCADE, related_name='history_channels')
    video      = models.ForeignKey('channel.Video', on_delete=models.CASCADE, related_name='history_videos')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'History by {0}'.format(self.channel.user.username)