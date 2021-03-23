from django.urls import path
from .views import FriendsView, ProfileFriend,send_friend_request, accept_friend_request

friends_urls = ([
    path('', FriendsView.as_view(), name='list'),
    path('<str:slug>/', ProfileFriend.as_view(), name='profile'),
    path('send_friend_request/<int:userID/', send_friend_request, name='Send_request'),
    path('accept_friend_request/<int:requestID>/', accept_friend_request, name='accept_request'),
], 'friends')