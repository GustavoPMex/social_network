from django.urls import path
from .views import FriendsView, ProfileFriend, SearchViewPerson, SearchViewFriends, RequestList, RequestSend, RequestCancel, RequestAccepted, RequestRemove, DeleteFriend, BlockUser, BlockList, UnblockUser

friends_urls = ([
    path('', FriendsView.as_view(), name='list'),
    path('search/', SearchViewPerson.as_view(), name='search'),
    path('search_list/', SearchViewFriends.as_view(), name='search_friend'),
    path('profile-person/<str:slug>/', ProfileFriend.as_view(), name='profile'),
    path('request-list/', RequestList.as_view(), name='request_list'),
    path('block-list/', BlockList.as_view(), name='block_list'),
    path('request-send/<slug:friend_name>/', RequestSend, name='request_send'),
    path('request-cancel/<str:friend_code>/', RequestCancel, name='request_cancel'),
    path('request-accepted/<int:id_relation>/<slug:friend_code>/', RequestAccepted, name='request_accepted'),
    path('request-remove/<int:id_relation>/<slug:friend_code>/', RequestRemove, name='request_remove'),
    path('delete-friend/<slug:friend_name>/', DeleteFriend, name='delete_friend'),
    path('block-user/<slug:friend_name>/', BlockUser, name='block_user'),
    path('unblock-user/<slug:friend_name>/', UnblockUser, name='unblock_user'),
], 'friends')