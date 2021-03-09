from django.urls import path
from .views import profile_view_base

urls_core = ([
    path('', profile_view_base, name='profile'),
], 'profile_core')