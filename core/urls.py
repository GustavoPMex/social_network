from django.urls import path
from .views import profile_core

urls_core = ([
    path('', profile_core, name='profile'),
], 'profile_core')