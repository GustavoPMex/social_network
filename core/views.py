from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from posts.models import PostUser
from posts.forms import PostUserForm
from django.urls import reverse_lazy


# Create your views here.

class CreatePost(CreateView):
    model = PostUser
    form_class = PostUserForm
    template_name = 'core/profile.html'
    success_url = reverse_lazy('profile_core:profile')
    
    def get_context_data(self, *args, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['posts'] = PostUser.objects.filter(owner=self.request.user)
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.like_post = 0
        obj.dislike_post = 0
        obj.save()
        return super(CreatePost, self).form_valid(form)