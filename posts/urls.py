from django.urls import path
from .views import create_post, DeletePost

post_urls = ([
    path('', create_post, name='create'),
    path('delete/<int:id_post>/<slug:slug_page>/', DeletePost, name='delete')
], 'post')