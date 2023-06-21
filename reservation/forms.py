from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Team, Event, Affiliation, Single



class MyUserCreationForm(UserCreationForm):
    # date_of_birth = forms.DateField(label='Date of birth',required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_of_birth','password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TeamCreationForm(ModelForm):
    # date_of_birth = forms.DateField(label='Date of birth',required=True)
    class Meta:
        model = Team
        fields = ['name']

class SingleForm(ModelForm):
    class Meta:
        model = Single
        fields = ['event']



# class UpdateTeam(forms.ModelForm):
#     username = forms.CharField(max_length=100,
#                                required=True,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(required=True,
#                              widget=forms.TextInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ['username', 'email']


class AffiliationForm(ModelForm):
    def __init__(self, *args, pk=None, teams_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_team'].queryset = teams_queryset

    class Meta:
        model = Affiliation
        fields = ['team_team']