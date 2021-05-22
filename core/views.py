from django.shortcuts import render
from django.views.generic import ListView
from posts.models import PostUser
from django.urls import reverse_lazy


# Create your views here.

class CreatePost(ListView):
    model = PostUser
    template_name = 'core/profile.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['posts'] = PostUser.objects.filter(owner=self.request.user)
        return context


