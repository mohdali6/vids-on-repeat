from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=15, primary_key=True)
    video_title = models.CharField(max_length=150)