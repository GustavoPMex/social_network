from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from registration.models import Profile
from .models import Relationship
from django.urls import reverse_lazy, reverse
from .forms import RelationshipForms
from django.db.models import Q
# Create your views here.  

# falanito - cq37zv
# Luis - 0yl6or
# Gustavo - 2fvu7d
# Fulanito - cwguhj

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class FriendsView(TemplateView):
    template_name = 'friends/friends.html'
    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        num_requests = Relationship.objects.filter(receiver__user_name__username=self.request.user, status='send').count()
        context['num_requests'] = num_requests
        return context

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
        #Se crearon dos opciones porque si el usuario actual es quien envia la solicitud, puede cancelarlo
        #y si es a quien se lo envian, pueden aceptarlo
        if relation_op_one:
            element_relation = relation_op_one.first()
            #Si el usuario es quien envia la solicitud
            if element_relation.status == 'send':
                context['relation'] = 'user_cancel'
                context['id_relation'] = element_relation.id
            else:
                context['relation'] = 'no_request'

        elif relation_op_two:
            #Si el usuario es que recibe la solicitud
            element_relation = relation_op_two.first()
            if element_relation.status == 'send':
                context['relation'] = 'user_accept'
                context['id_relation'] = element_relation.id
            else:
                context['relation'] = 'no_request'
        else:
            context['relation'] = 'request'

        return context

    def dispatch(self, request, *args, **kwargs):
        #Solicitamos el objeto del detail view
        obj = super(ProfileFriend, self).get_object()
        #Si el nombre del obj coincide con el usuario actual, redireccionamos a su profile
        if self.request.user == obj.user_name:
            return redirect('profile_core:profile')
        else:
            #En este caso es instancia de la clase profile, que tiene un atributo user_name
            relation_users = Relationship.objects.filter(Q(sender__user_name__username=obj.user_name,
                                                            receiver__user_name__username=self.request.user) | 
                                                          Q(sender__user_name__username=self.request.user,
                                                           receiver__user_name__username=obj.user_name))
            if relation_users:
                #Filtramos los values, pedimos el elemento en la posición 0 (que es un dict) y posteiormente pedimos el value con ayuda del key "status"
                relation_status = relation_users.first().status
                if relation_status == 'blocked':
                    return redirect('friends:list')
                else:
                    #En caso de que el estatus entre la relación no sea "blocked", muestra el perfil 
                    return super(ProfileFriend, self).dispatch(request, *args, **kwargs)
            else:
                #En caso de que no exista una relación se muestra el perfil de un usuario
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

def RequestSend(request, friend_name): 
    if request.method == 'POST':
        relation_users = Relationship.objects.filter(Q(sender__user_name__username=request.user,
                                                       receiver__user_name__username=friend_name) | 
                                                    Q(sender__user_name__username=friend_name,
                                                      receiver__user_name__username=request.user))
        if relation_users:
            return redirect('friends:list')
        else:
            #Buscamos si el usuario con el slug "friend_name" existe en el modelo Profile
            friend_obj = get_object_or_404(Profile, user_name__username=friend_name)
            if friend_obj.friend_user_code in request.META.get('HTTP_REFERER'):
                form = RelationshipForms(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.sender = request.user.profile
                    #Asignamos al receiver al usuario de friend_obj
                    form.receiver = friend_obj
                    form.status = 'send'
                    form.save()
                #Se redirecciona al mismo perfil
                return redirect(reverse_lazy('friends:profile', kwargs={'slug':friend_obj.friend_user_code}) + '?send')
            else:
                return HttpResponseForbidden()
    else:
        #Llamamos al form
        form = RelationshipForms()

    context = {
        'form':form,
        'username_request':friend_name,
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

    if obj_relationship.sender.friend_user_code == friend_by_code.friend_user_code:
        obj_relationship.status = 'accepted'
        obj_relationship.save()
        return redirect('friends:list')
    else:
        return HttpResponseForbidden()

def RequestRemove(request, id_relation, friend_code):
    current_user_code = request.user.profile.friend_user_code
    relation_request = Relationship.objects.filter(id=id_relation,
                                                   sender__friend_user_code=friend_code,
                                                   receiver__friend_user_code=current_user_code)
    if relation_request:
        relation_request.first().delete()
        return redirect('friends:request_list')
    else:
        return HttpResponseForbidden()

def DeleteFriend(request, friend_name):                

    if request.method == 'POST':       
        relation_users = Relationship.objects.filter(Q(sender__user_name__username=friend_name,
                                                      receiver__user_name__username=request.user) | 
                                                      #Si el primer filtro no se cumple, usamos éste segundo filtro. Todo ésto con ayuda de Q
                                                     Q(sender__user_name__username=request.user,
                                                      receiver__user_name__username=friend_name))

        if relation_users:
            #Tomamos el primer elemento en el queryset, éste caso solo hay una opción y la relación
            relation  = relation_users.first()
            relation.status = 'deleted'
            relation.save()
            relation.delete()
            return redirect('friends:list') 
        else:
            return HttpResponseForbidden()
    context = {
        'friend_name':friend_name
    }

    return render(request, 'friends/remove_friend.html', context)

def BlockUser(request, friend_name):
    if request.method == 'POST':
        relation_users = Relationship.objects.filter(Q(sender__user_name__username=friend_name,
                                                      receiver__user_name__username=request.user) | 
                                                    Q(sender__user_name__username=request.user,
                                                      receiver__user_name__username=friend_name))
        result = ''
        if relation_users:
            result = relation_users.first()
            #Comprobamos si el sender es igual al usuario que está realizando el bloqueo
            #Si no son el mismo, se cambian de posición el sender y el receiver
            if result.sender != request.user:
                result.sender = get_object_or_404(Profile, user_name__username=request.user)
                result.receiver = get_object_or_404(Profile, user_name__username=friend_name)
        else:
            #Si no existe una relacion, creamos una
            sender = get_object_or_404(Profile, user_name__username=request.user)
            receiver = get_object_or_404(Profile, user_name__username=friend_name)
            relation_create = Relationship.objects.create(sender=sender, receiver=receiver)
            result = relation_create
        #Cambiamos el status de la relación a blocked
        result.status = 'blocked'
        result.save()
        return redirect('friends:block_list')
    context = {
        'friend_name':friend_name
    }
    return render(request, 'friends/block_user.html', context)

def UnblockUser(request, friend_name):
    if request.method == 'POST':
        relation = Relationship.objects.filter(sender__user_name__username=request.user,
                                               receiver__user_name__username=friend_name).first()
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
        #Verificamos que se haya enviado algun elemento desde el search input
        if query:
            query_result = Profile.objects.filter(friend_user_code=query)
            if query_result:
                current_user = self.request.user
                friend = query_result.first().user_name
                relation_users = Relationship.objects.filter(Q(sender__user_name__username=current_user,
                                                             receiver__user_name__username=friend) | 
                                                             Q(sender__user_name__username=friend,
                                                             receiver__user_name__username=current_user))
                if relation_users:
                    #Si el status entre los usuarios NO es "blocked",  mostramos resultados
                    if relation_users.first().status != 'blocked':
                        result = query_result
                else:
                    #En dado caso que no haya una relación entre usuarios, simplemente mostramos el resultado
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
        #Verificamos si se obtiene algun elemento del input search
        if query:
            query_result = Profile.objects.filter(user_name__username__startswith=query)
            if query_result: 
                for element in query_result:
                    #Comprobamos si el usuario actual está en la lista de amigos del usuario que se está buscando
                    if self.request.user not in element.friends.all():
                        #Excluimos al usuario si no está en la lista de amigos
                        query_result = query_result.exclude(friend_user_code=element.friend_user_code)
                #Si despues de realizar la exclusión aun contamos con algun elemento, lo retornamos
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