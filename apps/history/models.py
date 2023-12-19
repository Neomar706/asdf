from django.db import models
from django.utils import timezone


class History(models.Model):
    channel = models.ForeignKey('channel.Channel', null=True, on_delete=models.CASCADE, related_name='history_channels')
    videos = models.ManyToManyField('channel.Video', blank=True, related_name='history_videos')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'History by {0}'.format(self.channel.user.username)