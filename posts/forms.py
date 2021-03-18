from django import forms
from .models import PostUser

class PostUserForm(forms.ModelForm):
    class Meta:
        model = PostUser
        fields = ['post_user']
        labels = {'post_user': ''}
        widgets = {
            'post_user':forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':"What's up?"}),
        }