from django.db import models
from django.contrib.auth.models import User
from registration.models import Profile

# Create your models here.

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
    ('deleted', 'deleted'),
    ('blocked', 'blocked')
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} - {self.receiver} - {self.status}'


