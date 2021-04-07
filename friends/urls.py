from django.urls import path
from .views import FriendsView, ProfileFriend, SearchViewPerson, SearchViewFriends, RequestList, RequestSend

friends_urls = ([
    path('', FriendsView.as_view(), name='list'),
    path('search/', SearchViewPerson.as_view(), name='search'),
    path('search_list/', SearchViewFriends.as_view(), name='search_friend'),
    path('profile-person/<str:slug>/', ProfileFriend.as_view(), name='profile'),
    path('request-list/', RequestList.as_view(), name='request_list'),
    path('request-send/<str:slug>/', RequestSend, name='request_send')
], 'friends')