from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from .models import FriendRequest
from django.views.generic import ListView, DetailView
from .models import UserFriends
from registration.models import Profile
# Create your views here.  zqaatw

 
class FriendsView(ListView):
    model = UserFriends
    template_name = 'friends/friends.html'
    context_object_name = 'list_friends'

class ProfileFriend(DetailView):
    slug_field = 'friend_user_code'
    model = Profile
    template_name = 'friends/friend_profile.html'

class SearchView(ListView):
    model = Profile
    template_name = 'friends/search_friend_profile.html'
    context_object_name = 'friend'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')

        print('Hola')
        print(query)

        if query:
            postresult = Profile.objects.filter(friend_user_code__contains=query)

            if postresult:
                result = postresult
            else:
                result = 'no results'
        else:
            result = 'no results'
        
        return result
    
    


def send_friend_request(request, userID):
    from_user = request.user 
    to_user = User.objects.get(id=userID)

    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )

    if created:
        return httpResponse('Friend request sent')
    else:
        return httpResponse('Friend request was already sent')
    

def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_reques.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted')
    else:
        return HttpResponse('Friend request not accepted')