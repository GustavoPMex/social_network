from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import PostUser
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

def create_post(request):
    post = request.GET.get('post')
    previous_url = request.META.get('HTTP_REFERER')

    if post:
        PostUser.objects.create(owner=request.user, post_user=post,
                                like_post=0, dislike_post=0)
    
    return redirect(previous_url)


def DeletePost(request, id_post, slug_page):
    if request.method == 'POST':
        post = get_object_or_404(PostUser, id=id_post)
        post.delete()

        if "news" in request.path:
            return redirect('news:home')
        else:
            return redirect('profile_core:profile')

    context = {
        'id_post':id_post,
        'slug':slug_page
    }

    return render(request, 'posts/delete_post.html', context)