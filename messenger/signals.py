from django.db.models.signals import pre_delete
from .models import Thread
from django.dispatch import receiver


@receiver(pre_delete, sender=Thread)
def pre_revision_commit(sender, instance, **kwargs):
    for msgs in instance.messages.all():
        msgs.delete()