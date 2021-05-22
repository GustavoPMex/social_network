from django.urls import path
from .views import news_home

news_urls = ([
    path('', news_home, name='home'),
], 'news')