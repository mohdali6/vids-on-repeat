from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=15, primary_key=True)
    video_title = models.CharField(max_length=150)

    def __str__(self):
        return self.video_title


class VideoRepeats(models.Model):
    repeat_count = models.IntegerField(default=0)
    video = models.OneToOneField(Video)

    class Meta:
        ordering = ('-repeat_count',)

    def __str__(self):
        return self.video.video_title