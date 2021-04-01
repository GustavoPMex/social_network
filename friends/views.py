from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, TemplateView
from registration.models import Profile
from .models import Relationship
# Create your views here.  cwguhj
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
 
class FriendsView(TemplateView):
    template_name = 'friends/friends.html'

class ProfileFriend(DetailView):
    slug_field = 'friend_user_code'
    model = Profile
    template_name = 'friends/friend_profile.html'

class SearchViewPerson(ListView):

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

            for element in query_result:
                if self.request.user not in element.friends.all():
                    query_result = query_result.exclude(id=element.id)

            if query_result: 
                result = query_result
            else:
                result = 'no results' 
        else:
            result = 'no results'
        
        return result


