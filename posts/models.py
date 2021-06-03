from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class PostUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_user = models.TextField()
    date_post = models.DateTimeField(auto_now_add=True)
    like_post = models.ManyToManyField(User, related_name='likes', blank=True)
    dislike_post = models.ManyToManyField(User, related_name='dislikes', blank=True)

    def __str__(self):
        return str(self.owner)

    def total_likes(self):
        return self.like_post.count()
    
    def total_dislikes(self):
        return self.dislike_post.count()
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-date_post']
