from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=50, default='no_id')
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    type = models.CharField(max_length=50)
    top_rank = models.IntegerField()
    image = models.URLField()
    duration = models.IntegerField()
    rating = models.FloatField()
    genres = models.JSONField()
    some_plot = models.TextField()
    full_plot = models.TextField()
    is_watched = models.BooleanField(default=False)
    def __str__(self):
        return self.title
