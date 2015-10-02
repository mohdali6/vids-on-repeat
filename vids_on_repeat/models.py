from django.db import models

from django.contrib.sessions.models import Session


class Video(models.Model):
    video_id = models.CharField(max_length=15, primary_key=True)
    video_title = models.CharField(max_length=150)

    def __str__(self):
        return self.video_title


class VideoRepeats(models.Model):
    video = models.OneToOneField(Video, primary_key=True)
    repeat_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-repeat_count',)

    def __str__(self):
        return self.video.video_title


class SessionBasedRepeats(models.Model):
    video = models.ForeignKey(Video)
    session = models.ForeignKey(Session)
    repeat_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('video', 'session')