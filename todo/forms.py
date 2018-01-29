from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'E-mail address'}))
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    class Meta:
        model=User
        fields=('first_name','last_name','email','username','password1','password2')
