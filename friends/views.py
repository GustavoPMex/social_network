from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
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


    def get_object(self, *args, **kwargs):
        obj = super(ProfileFriend, self).get_object(*args,**kwargs)
        relation = get_object_or_404(Relationship, sender__user_name__username=obj.user_name, receiver__user_name__username=self.request.user)
        if relation.status == 'blocked':
            return HttpResponseNotAllowed(['GET', 'POST']) 
        else:
            return obj

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
        # return redirect(reverse_lazy('friends:profile', slug=user_in_profile.profile.friend_user_code) + '?send')
        return redirect(reverse_lazy('friends:profile', kwargs={'slug':user_in_profile.profile.friend_user_code}) + '?send')

    else:
        form = RelationshipForms()

    context = {
        'form':form,
        'username_request':slug,
    }
    
    return render(request, 'friends/send_request.html', context)

def RequestAccepted(request, id_relation, friend_code):
    obj_relationship = get_object_or_404(Relationship, id=id_relation)
    friend_by_code = get_object_or_404(Profile,  friend_user_code=friend_code)

    if obj_relationship.sender.friend_user_code == friend_code:
        obj_relationship.status = 'accepted'
        obj_relationship.save()
        return redirect('friends:list')

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    
def RequestRemove(request, id_relation, friend_code):
    obj_relationship = get_object_or_404(Relationship, id=id_relation)
    friend_by_code = get_object_or_404(Profile, friend_user_code=friend_code)

    if obj_relationship.sender.friend_user_code == friend_code:
        obj_relationship.delete()
        return redirect('friends:request_list')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def DeleteFriend(request, friend_name):   
    if request.method == 'POST':
        #Primera forma
        # try:
        #     relation = Relationship.objects.get(sender__user_name__username=friend_name, receiver__user_name__username=request.user)
        # except Relationship.DoesNotExist:
        #     return HttpResponseNotAllowed(['GET', 'POST'])

        relation = get_object_or_404(Relationship, sender__user_name__username=friend_name, receiver__user_name__username=request.user)

        relation.status = 'deleted'
        relation.save()
        relation.delete()

        return redirect('friends:list') 

    context = {
        'friend_name':friend_name
    }

    return render(request, 'friends/remove_friend.html', context)

def BlockUser(request, friend_name):
    if request.method == 'POST':
        relation = get_object_or_404(Relationship, sender__user_name__username=friend_name, receiver__user_name__username=request.user)
        relation.status = 'blocked'
        relation.save()
        return redirect('friends:list')

    context = {
        'friend_name':friend_name
    }

    return render(request, 'friends/block_user.html', context)

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


