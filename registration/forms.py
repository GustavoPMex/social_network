from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Max Length: 254 Characters')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already registered')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['friend_user_code',
                'img_profile',
                'intro',
                'birthday',
                'nationality',
                'sn_github',
                'sn_twitter',
                'sn_youtube']
        
        widgets = {
            'friend_user_code':forms.TextInput(attrs={'class':'form-control  my-3  mx-auto', 'placeholder':'friend_user_code','style':'pointer-events:none;'}),
            'img_profile':forms.ClearableFileInput(attrs={'class':'form-control my-3  mx-auto'}),
            'intro':forms.Textarea(attrs={'class':'form-control  my-3  mx-auto', 'rows':3, 'placeholder':'Intro'}),
            'birthday':forms.DateInput(attrs={'class':'form-control  my-3  mx-auto','placeholder':'DD/MM/YYYY'}),
            'nationality':forms.TextInput(attrs={'class':'form-control  my-3  mx-auto', 'placeholder':'Nationality'}),
            'sn_github':forms.URLInput(attrs={'class':'form-control  my-3  mx-auto','placeholder':'Github url'}),
            'sn_twitter':forms.URLInput(attrs={'class':'form-control  my-3  mx-auto','placeholder':'Twitter url'}),
            'sn_youtube':forms.URLInput(attrs={'class':'form-control  my-3  mx-auto', 'placeholder':'Youtube url'})
        }