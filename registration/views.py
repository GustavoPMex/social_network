from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django import forms
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from .models import Profile

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register' 

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        #Modificar en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Repeat your Password'})
        return form

class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile_core:profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user_name=self.request.user)
        return profile

class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'})
        return form