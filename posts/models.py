from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PostUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_user = models.TextField()
    date_post = models.DateTimeField(auto_now_add=True)
    like_post = models.DecimalField(decimal_places=0, max_digits=100)
    dislike_post = models.DecimalField(decimal_places=0, max_digits=100)

    def __str__(self):
        return str(self.owner)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-date_post']
