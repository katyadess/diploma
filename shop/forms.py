from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm


class SubscribeForm(forms.ModelForm):
    
    class Meta: 
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs= {
            'placeholder': 'Enter your email...',
            })
        }