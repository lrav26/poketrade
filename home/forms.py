from django import forms
from .models import Pokemon

class NicknameForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['nickname']