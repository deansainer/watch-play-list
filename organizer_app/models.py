from django.db import models
# 'content_id': response['d'][0]['id'],
#           'content_name': response['d'][0]['l'],
#           'content_image': response['d'][0]['i']['imageUrl'],
#           'content_type': response['d'][0]['qid'],
#           'release_year': response['d'][0]['y'],
class Content(models.Model):
    content_id = models.CharField(max_length=255, unique=True)
    content_name = models.CharField(max_length=255, unique=True)
    content_image = models.URLField()
    content_type = models.CharField(max_length=55)
    release_year = models.IntegerField()

    def __str__(self):
        return self.content_name
