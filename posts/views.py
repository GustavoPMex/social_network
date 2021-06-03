from django.http import JsonResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import PostUser

def create_post(request):
    post = request.GET.get('post')
    previous_url = request.META.get('HTTP_REFERER')

    if post:
        PostUser.objects.create(owner=request.user, post_user=post)
    
    return redirect(previous_url)

def DeletePost(request, id_post, slug_page):

    if request.method == 'POST':
        post = get_object_or_404(PostUser, id=id_post)
        post.delete()

        if "news" in request.path:
            return redirect('news:home')
        elif "profile" in request.path:
            return redirect('profile_core:profile')
        else:
            return HttpResponseForbidden()

    context = {
        'id_post':id_post,
        'slug':slug_page
    }

    return render(request, 'posts/delete_post.html', context)


def reactions_post(request, id_post, reaction):
    post = get_object_or_404(PostUser, id=id_post)
    current_user = request.user
    liked = False
    disliked = False

    if reaction == 'like':
        if current_user not in post.like_post.all():
            post.like_post.add(current_user)
            liked = True
            if current_user in post.dislike_post.all():
                post.dislike_post.remove(current_user)
        else:
            post.like_post.remove(current_user)
        post.save()

    elif reaction == 'dislike':
        if current_user not in post.dislike_post.all():
            post.dislike_post.add(current_user)
            disliked = True
            if current_user in post.like_post.all():
                post.like_post.remove(current_user)
        else:
            post.dislike_post.remove(current_user)
        post.save() 
    else:
        return HttpResponseForbidden()
    
    reaction_json = {
        'liked':liked,
        'disliked':disliked,
        'total_likes':post.total_likes(),
        'total_dislikes':post.total_dislikes()
    }

    return JsonResponse(reaction_json)
