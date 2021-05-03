from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

class ThreadManager(models.Manager):
    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0:
            return queryset[0]
        return None
    
    def find_or_create(self, user1, user2):
        thread = self.find(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread

class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadManager()

    class Meta:
        ordering = ['-updated']

def messages_changed(sender, **kwargs):
    #Recuperamos el thread al que le deseamos añadir los mensajes
    instance = kwargs.pop('instance', None)
    #La accion que se ejecuta
    action = kwargs.pop('action', None)
    #Referencia a un conjuntos de los mensajes
    pk_set = kwargs.pop('pk_set', None)

    #En éste set se añadiran los elementos que no formen parte del thread
    false_pk_set = set()

    if action is 'pre_add':
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print('No forma parte del thread')
                false_pk_set.add(msg_pk)
    
    #Buscar los mensajes de false_pk_set que están en pk_set y los borramos de pk_set
    pk_set.difference_update(false_pk_set)

    #Forzar actualizacion haciendo un save
    instance.save()

#Detectamos cualquier cambio que ocurra en "messages" de una instancia de Thread
m2m_changed.connect(messages_changed, sender=Thread.messages.through)