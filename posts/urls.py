from django.urls import path
from .views import create_post, DeletePost, reactions_post

post_urls = ([
    path('', create_post, name='create'),
    path('delete/<int:id_post>/<slug:slug_page>/', DeletePost, name='delete'),
    path('reaction/<int:id_post>/<slug:reaction>/', reactions_post, name='reaction')
], 'post')