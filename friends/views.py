from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from registration.models import Profile
from .models import Relationship
from django.urls import reverse_lazy
from .forms import RelationshipForms

# Create your views here.  cwguhj

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
 
class FriendsView(TemplateView):
    template_name = 'friends/friends.html'

class ProfileFriend(DetailView):
    slug_field = 'friend_user_code'
    model = Profile
    template_name = 'friends/friend_profile.html'

class RequestList(ListView):
    model = Relationship
    template_name = 'friends/friends_request.html'
    context_object_name = 'requests'

    def get_queryset(self):
        result = Relationship.objects.filter(receiver__user_name__username=self.request.user, status='send')
        return result


def RequestSend(request, slug):
    # Pruebas con ayuda del GET
    # if request.method == 'GET':
    #     pass
        
    if request.method == 'POST':
        form = RelationshipForms(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.sender = request.user.profile
            
            #Filtrando al usuario que tenga coincidencia con el nombre que se le pasó atraves del slug
            user_in_profile = Profile.objects.only('user_name').get(user_name__username=slug).user_name
            #Pasamos la instancia del usuario del profile
            form.receiver = user_in_profile.profile

            form.status = 'send'

            form.save()

        #Se redirecciona al mismo perfil
        return redirect('friends:profile', slug=user_in_profile.profile.friend_user_code)

    else:
        form = RelationshipForms()

    context = {
        'form':form,
        'username_request':slug,
    }
    
    return render(request, 'friends/send_request.html', context)

# class RequestSend(CreateView):
#     model = Relationship
#     form_class = RelationshipForms
#     template_name = 'friends/send_request.html'
    
#     def get_success_url(self):
#         return reverse_lazy('friends:list')

#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.sender = self.request.user.profile
#         receiver_contain = Relationship.object.get(receiver=self.kwargs.get('slug', None))
#         print(receiver_contain)
#         obj.status = 'send'
#         return super(RequestSend, self).form_valid(form)

 
class SearchViewPerson(ListView):
    model = Profile
    template_name = 'friends/search_friend_profile.html'
    context_object_name = 'list_results'

    def get_queryset(self):
        query = super(SearchViewPerson, self).get_queryset()
        query = self.request.GET.get('search')

        if query:
            query_result = Profile.objects.filter(friend_user_code=query)

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
    context_object_name = 'list_friends'

    def get_queryset(self):
        query = self.request.GET.get('search_friend')

        if query:
            query_result = Profile.objects.filter(user_name__username__startswith=query)

            if query_result: 

                for element in query_result:
                    if self.request.user not in element.friends.all():
                        query_result = query_result.exclude(friend_user_code=element.friend_user_code)

                if query_result:
                    result = query_result
                else:
                    result = 'no results'
            else:
                result = 'no results' 
        else:
            result = 'no results'
        
        return result


