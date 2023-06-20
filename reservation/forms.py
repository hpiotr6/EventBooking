from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User



class MyUserCreationForm(UserCreationForm):
    # date_of_birth = forms.DateField(label='Date of birth',required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_of_birth','password1', 'password2']



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']