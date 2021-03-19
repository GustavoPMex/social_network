from django.urls import path
from .views import CreatePost, DeletePost

urls_core = ([
    path('', CreatePost.as_view(), name='profile'),
    path('profile/delete/<int:pk>/', DeletePost.as_view(), name='delete')
], 'profile_core')