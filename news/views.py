from django.shortcuts import render
from posts.models import PostUser
from datetime import date, timedelta

# Create your views here.

def news_home(request):
    #2021-05-20
    #filtrar solamente por fecha
    today = date.today()
    two_days_ago = today - timedelta(days=2)
    post_on_date = PostUser.objects.filter(date_post__date__range=[two_days_ago, today])
    
    context = {
        'post_on_date':post_on_date

    }

    return render(request, 'news/news.html', context)


