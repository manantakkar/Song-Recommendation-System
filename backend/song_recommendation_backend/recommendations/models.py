
from django.db import models

class RecommendationScheme(models.Model):
    artist_name = models.CharField(max_length=255)
    genres = models.JSONField()
    attrs = models.JSONField()

class Music(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    artist = models.CharField(max_length=255)
    image_link = models.URLField()