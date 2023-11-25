from django.db import models
from django.utils import timezone
from apps.channel.models import Channel, Video


class Comment(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='comment_channel')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comment_video')
    content = models.TextField()
    likes = models.ManyToManyField(Channel, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(Channel, blank=True, related_name='comment_dislikes')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0} - {1}'.format(self.channel.name, self.content)