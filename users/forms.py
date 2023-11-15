# forms.py in the 'users' app

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    # Add an email field to the UserCreationForm
    email = forms.EmailField()

    class Meta:
        # Set the model to User and specify the fields to include in the form
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUsernameForm(forms.Form):
    # Define a form for updating the username
    new_username = forms.CharField(
        max_length=150, required=True, label='New Username')


class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        # Set the model to UserProfile and specify the field for updating the profile picture
        model = UserProfile
        fields = ['profile_picture']
