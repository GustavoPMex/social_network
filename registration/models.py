from django.db import models
from django.contrib.auth.models import User
from .utils import code_generator, create_shortcode
import datetime
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_user_code = models.CharField(max_length=15, unique=True, blank=True)
    img_profile = models.ImageField(upload_to = 'profiles', null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, default=datetime.date.today)
    nationality = models.CharField(max_length=100)
    sn_github = models.CharField(max_length=100, null=True, blank=True)
    sn_twitter = models.CharField(max_length=100, null=True, blank=True)
    sn_youtube = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.friend_user_code is None or self.friend_user_code == "":
            self.friend_user_code = create_shortcode(self)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user_name)