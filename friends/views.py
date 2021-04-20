from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from registration.models import Profile
from .models import Relationship
from django.urls import reverse_lazy
from .forms import RelationshipForms

# Create your views here.  

# falanito - cq37zv
# Luis - 0yl6or
# Gustavo - 2fvu7d
# Fulanito - cwguhj

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
 
class FriendsView(TemplateView):
    template_name = 'friends/friends.html'

class ProfileFriend(DetailView):
    model = Profile
    slug_field = 'friend_user_code'
    template_name = 'friends/friend_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileFriend, self).get_context_data(**kwargs)
        current_user = self.request.user
        friend_user = context['object'].user_name

        relation_op_one = Relationship.objects.filter(sender__user_name__username = current_user,
                                                      receiver__user_name__username = friend_user)
        relation_op_two = Relationship.objects.filter(sender__user_name__username=friend_user,
                                                      receiver__user_name__username=current_user)
        
        if relation_op_one:
            element_relation = relation_op_one.first()
            if element_relation.status == 'send':
                context['relation'] = 'user_cancel'
                context['id_relation'] = element_relation.id
            else:
                context['relation'] = 'no_request'

        elif relation_op_two:
            element_relation = relation_op_two.first()
            if element_relation.status == 'send':
                context['relation'] = 'user_accept'
                context['id_relation'] = element_relation.id
            else:
                context['relation'] = 'no_request'

        return context

    def dispatch(self, request, *args, **kwargs):
        #Solicitamos el objeto del detail view
        obj = super(ProfileFriend, self).get_object()
        #Si el nombre del obj coincide con el usuario actual, redireccionamos a su profile
        if self.request.user == obj.user_name:
            return redirect('profile_core:profile')
        else:
            #En este caso es instancia de la clase profile, que tiene un atributo user_name
            relation_op_one = Relationship.objects.filter(sender__user_name__username=obj.user_name, receiver__user_name__username=self.request.user)
            #En este caso es instancia de la clase profile, que tiene un atributo user_name
            #La razon de por qué se piden dos filter, es por que el sender y receiver pueden variar de posición, dependiendo quien envió la solicitud de amistad
            relation_op_two = Relationship.objects.filter(sender__user_name__username=self.request.user, receiver__user_name__username=obj.user_name)
            #Declaramos result
            result = ''

            if relation_op_one:
                #Filtramos los values, pedimos el elemento en la posición 0 (que es un dict) y posteiormente pedimos el value con ayuda del key "status"
                result = relation_op_one.values("status")[0]['status']
            elif relation_op_two:
                #Filtramos los values, pedimos el elemento en la posición 0 (que es un dict) y posteiormente pedimos el value con ayuda del key "status"
                result = relation_op_two.values("status")[0]['status']
            else:
                #En caso de que ninguno se cumpla, se prohibe la entrada
                return super(ProfileFriend, self).dispatch(request, *args, **kwargs)

            if result == 'blocked':
                #Si el objeto filtrado(status) es blocked, se redirecciona a la lista de amigos
                return redirect('friends:list')
            else:
                #Retornamos del objeto de detail view de manera normal
                return super(ProfileFriend, self).dispatch(request, *args, **kwargs)

class RequestList(ListView):
    model = Relationship
    template_name = 'friends/friends_request.html'
    context_object_name = 'requests'

    def get_queryset(self):
        result = Relationship.objects.filter(receiver__user_name__username=self.request.user, status='send')
        return result

class BlockList(ListView):
    model = Relationship
    template_name = 'friends/block_list.html'
    context_object_name = 'blocks'

    def get_queryset(self):
        result = Relationship.objects.filter(sender__user_name__username=self.request.user, status='blocked')
        return result

def RequestSend(request, slug): 
    if request.method == 'POST':
        relation_op_one = Relationship.objects.filter(sender__user_name__username=request.user, receiver__user_name__username=slug)
        relation_op_two = Relationship.objects.filter(sender__user_name__username=slug, receiver__user_name__username=request.user)
        if relation_op_one or relation_op_two:
            return redirect('friends:list')
        else:
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

def RequestCancel(request, friend_code):
    current_user_code = request.user.profile.friend_user_code
    relation_friend = Relationship.objects.filter(sender__friend_user_code=current_user_code,
                                                  receiver__friend_user_code=friend_code)
    if relation_friend:
        relation_friend.delete()
        return redirect(reverse_lazy('friends:profile', kwargs={'slug':friend_code})) 
    else:
        return HttpResponseForbidden()

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
    current_user_code = request.user.profile.friend_user_code
    relation_request = Relationship.objects.filter(id=id_relation,
                                                   sender__friend_user_code=friend_code,
                                                   receiver__friend_user_code=current_user_code)

    if relation_request:
        relation_request.first().delete()
        return redirect('friends:request_list')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def DeleteFriend(request, friend_name):               
    if request.method == 'POST':
        relation_op_one = Relationship.objects.filter(sender__user_name__username=friend_name, receiver__user_name__username=request.user)
        relation_op_two = Relationship.objects.filter(sender__user_name__username=request.user, receiver__user_name__username=friend_name)
        result = ''

        if relation_op_one:
            result  = relation_op_one.get(status='accepted')
        elif relation_op_two:
            result = relation_op_two.get(status='accepted')
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])

        result.status = 'deleted'
        result.save()
        result.delete()
        return redirect('friends:list') 

    context = {
        'friend_name':friend_name
    }

    return render(request, 'friends/remove_friend.html', context)

def BlockUser(request, friend_name):
    if request.method == 'POST':
        relation_op_one = Relationship.objects.filter(sender__user_name__username=friend_name, receiver__user_name__username=request.user)
        relation_op_two = Relationship.objects.filter(sender__user_name__username=request.user, receiver__user_name__username=friend_name)
        result = ''

        if relation_op_one:
            result = relation_op_one.first()
        elif relation_op_two:
            result = relation_op_two.first()
        else:
            sender = get_object_or_404(Profile, user_name__username=request.user)
            receiver = get_object_or_404(Profile, user_name__username=friend_name)
            relation_create = Relationship.objects.create(sender=sender, receiver=receiver)
            result = relation_create
    
        if result.sender != request.user:
            result.sender = get_object_or_404(Profile, user_name__username=request.user)
            result.receiver = get_object_or_404(Profile, user_name__username=friend_name)
        
        result.status = 'blocked'
        result.save()
        return redirect('friends:list')

    context = {
        'friend_name':friend_name
    }

    return render(request, 'friends/block_user.html', context)

def UnblockUser(request, friend_name):
    if request.method == 'POST':
        relation = Relationship.objects.filter(sender__user_name__username=request.user, receiver__user_name__username=friend_name).first()
        relation.delete()
        return redirect('friends:block_list')
    context = {
        'friend_name':friend_name
    }

    return render(request, 'friends/unblock_user.html', context)
 
class SearchViewPerson(ListView):
    model = Profile
    template_name = 'friends/search_friend_profile.html'
    context_object_name = 'list_results'

    def get_queryset(self):
        query = self.request.GET.get('search')
        #El valor por default será "no results"
        result = 'no results'

        if query:
            query_result = Profile.objects.filter(friend_user_code=query)
            current_user = self.request.user
            query_friend = query_result.first()

            if query_result:
                relation_op_one = Relationship.objects.filter(sender__user_name__username=current_user,
                                                             receiver__user_name__username=query_friend.user_name)
                relation_op_two = Relationship.objects.filter(sender__user_name__username=query_friend.user_name,
                                                             receiver__user_name__username=current_user)
                #Si el usuario está autorizado, es decir que no esté bloqueado, mostramos resultado de la busqueda
                auth_user = True

                #En éstas condiciones, si el usuario tiene status "blocked", entonces reasignamos el valor a False para negar el permiso
                if relation_op_one:
                    if relation_op_one.first().status == 'blocked':
                        auth_user = False

                elif relation_op_two:
                    if relation_op_two.first().status == 'blocked':
                        auth_user = False
                
                #Verificamos que el usuario esté autorizado
                if auth_user:
                    result = query_result
        
        return result
       
class SearchViewFriends(ListView):
    model = Profile
    template_name = 'friends/search_friend_list.html'
    context_object_name = 'list_friends'

    def get_queryset(self):
        query = self.request.GET.get('search_friend')
        #El valor predeterminado será "no results"
        result = 'no results'
        if query:
            query_result = Profile.objects.filter(user_name__username__startswith=query)
            if query_result: 
                for element in query_result:
                    #Comprobamos si el usuario actual está en la lista de amigos del usuario que se está buscando
                    if self.request.user not in element.friends.all():
                        #Excluimos al usuario si no está en la lista de amigos
                        query_result = query_result.exclude(friend_user_code=element.friend_user_code)
                if query_result:
                    result = query_result
        
        return result


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