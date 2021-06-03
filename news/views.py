from django.shortcuts import render
from posts.models import PostUser
from registration.models import Profile
from datetime import date, timedelta
# Create your views here.

def news_home(request):
    #filtrar solamente por fecha
    today = date.today()
    two_days_ago = today - timedelta(days=2)
    post_on_date = PostUser.objects.filter(date_post__date__range=[two_days_ago, today])

    #Filtrar por amigos
    friends = request.user.profile.friends.all()

    for post in post_on_date:
        if post.owner not in friends and post.owner != request.user:
            post_on_date = post_on_date.exclude(owner=post.owner)
    
    context = {
        'post_on_date':post_on_date
    }

    return render(request, 'news/news.html', context)


