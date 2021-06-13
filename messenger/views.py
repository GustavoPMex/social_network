from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import Thread, Message
from django.http import Http404, JsonResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class ThreadList(TemplateView):
    template_name = 'messenger/thread_list.html'

class ThreadDetail(DetailView):
    model = Thread

    def get_object(self):
        obj = super(ThreadDetail, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404
        return obj

class DeleteThread(DeleteView):
    model = Thread
    template_name = 'messenger/delete_chat.html'
    success_url = reverse_lazy('messenger:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if self.object:
            for message in self.object.messages.all():
                if message.user == self.request.user:
                    message.delete()
                
            if self.object.messages.all():
                return HttpResponseRedirect(reverse_lazy('messenger:detail', kwargs={'pk':self.object.id}))
        
        return HttpResponseRedirect(self.get_success_url())
        

def add_message(request, pk):
    json_response = {'created':False}

    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created']=True
            if len(thread.messages.all()) is 1:
                json_response['first']=True
    else:
        raise Http404('User is not authenticated')
    
    return JsonResponse(json_response)

def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
