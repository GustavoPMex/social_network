from django.urls import path
from .views import CreatePost

urls_core = ([
    path('profile/', CreatePost.as_view(), name='profile'),
], 'profile_core')