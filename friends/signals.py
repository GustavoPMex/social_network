from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Relationship

@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver

    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user_name)
        receiver_.friends.add(sender_.user_name)
        sender_.save()
        receiver_.save()

    elif instance.status == 'deleted':
        sender_.friends.remove(receiver_.user_name)
        receiver_.friends.remove(sender_.user_name)
        sender_.save()
        receiver_.save()
    
    elif instance.status == 'blocked':
        sender_.friends.remove(receiver_.user_name)
        receiver_.friends.remove(sender_.user_name)
        sender_.save()
        receiver_.save()