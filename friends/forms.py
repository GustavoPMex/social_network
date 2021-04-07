from django import forms
from .models import Relationship


class RelationshipForms(forms.ModelForm):
    class Meta: 
        model = Relationship
        fields = []