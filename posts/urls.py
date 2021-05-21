from django.urls import path
from .views import create_post

post_urls = ([
    path('', create_post, name='create')
], 'post')