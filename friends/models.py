from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserFriends(AbstractUser):
    friends = models.ManyToManyField("UserFriends", blank=True)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserFriends, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserFriends, related_name='to_user', on_delete=models.CASCADE)

