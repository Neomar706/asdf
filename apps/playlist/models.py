from django.db import models
from django.utils import timezone
from uuid import uuid4 as uuid


def thumbnail_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return 'thumbnails/{0}/{1}.{2}'.format(instance.channel.user, uuid(), extension)


class Playlist(models.Model):
    channel = models.ForeignKey('channel.Channel', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to=thumbnail_directory_path, default='image_1.jpg')
    duration = models.DurationField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    videos = models.ManyToManyField('channel.Video', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'channel/{0} - {1} - {2}'.format(self.channel.id, self.channel.user.username, self.title)