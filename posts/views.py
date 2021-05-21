from django.shortcuts import render, redirect
from .models import PostUser

def create_post(request):
    post = request.GET.get('post')
    previous_url = request.META.get('HTTP_REFERER')

    if post:
        PostUser.objects.create(owner=request.user, post_user=post,
                                like_post=0, dislike_post=0)
    
    return redirect(previous_url)


    