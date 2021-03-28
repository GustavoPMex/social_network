from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from .models import FriendRequest, UserFriends
from django.views.generic import ListView, DetailView
from registration.models import Profile
# Create your views here.  zqaatw
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
 
class FriendsView(ListView):
    model = UserFriends
    template_name = 'friends/friends.html'
    context_object_name = 'list_friends'

class ProfileFriend(DetailView):
    slug_field = 'friend_user_code'
    model = Profile
    template_name = 'friends/friend_profile.html'

class SearchViewPerson(ListView):
    model = Profile
    template_name = 'friends/search_friend_profile.html'
    context_object_name = 'friend'

    def get_queryset(self):
        result = super(SearchViewPerson, self).get_queryset()
        query = self.request.GET.get('search')

        if query:
            query_result = Profile.objects.filter(friend_user_code__contains=query)

            if query_result:
                result = query_result
            else:
                result = 'no results'
        else:
            result = 'no results'
        
        return result
    
    
class SearchViewFriends(ListView):
    model = Profile
    template_name = 'friends/search_friend_list.html'
    context_object_name = 'list_results'

    def get_queryset(self):
        query = super(SearchViewFriends, self).get_queryset()
        query = self.request.GET.get('search_friend')

        if query:
            query_result = Profile.objects.filter(user_name__username__contains=query) 

            if query_result:
                result = query_result 
            else:
                result = 'no results'
        else:
            result = 'no results'
        
        return result

def send_friend_request(request, userID):
    from_user = request.user 
    to_user = get_user_model().objects.get(id=userID)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('Friend request sent')
    else:
        return HttpResponse('Friend request was already sent')
    

def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted')
    else:
        return HttpResponse('Friend request not accepted')