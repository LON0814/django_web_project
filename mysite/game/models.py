from django.db import models
from embed_video.fields import EmbedVideoField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from config import settings

# Create your models here.
class Game(models.Model):
    app_id = models.IntegerField(verbose_name='app_id', null=True, blank=True)
    title = models.CharField(verbose_name='title', max_length=100)
    genre = models.CharField(verbose_name='genre', max_length=100)
    developer = models.CharField(verbose_name='developer', max_length=100)
    release_at = models.DateTimeField(verbose_name='release Day')
    info = models.TextField(verbose_name='info')
    video = EmbedVideoField(null=True)

    thumbnail = ProcessedImageField(
        upload_to='thumbnail',
        processors=[ResizeToFill(220, 70)],
        format='JPEG',
        options={'qualtiy': 80},
        blank=True
    )
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_game')
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Genre_list(models.Model):
    genre_list = models.CharField(verbose_name='genre_list', max_length=100)

    def __str__(self):
        return self.genre_list


class Comment(models.Model):
    post= models.ForeignKey(Game, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_date= models.DateTimeField(auto_now_add=True)
    comment_contents=models.CharField(max_length=200)
    comment_writer= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='game_comment_writer')

    class Meta:
        ordering=['-id']