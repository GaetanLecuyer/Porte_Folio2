# views.py in the 'users' app

from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UpdateUsernameForm, UpdateProfilePictureForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import IntegrityError


class RegisterView(View):
    """
    View to handle user registration.

    GET: Render the registration form.
    POST: Process the registration form and create a new user.
    """

    def get(self, request):
        form = UserRegisterForm()
        update_form = UpdateProfilePictureForm()
        return render(request, 'users/register.html', {'form': form, 'update_form': update_form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        update_form = UpdateProfilePictureForm(request.POST, request.FILES)

        if form.is_valid() and update_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            profile_picture = update_form.cleaned_data['profile_picture']

            if hasattr(user, 'userprofile'):
                user.userprofile.profile_picture = profile_picture
            else:
                UserProfile.objects.create(
                    user=user, profile_picture=profile_picture)

            user.save()
            user.userprofile.save()

            return redirect('index')

        else:
            return render(request, 'users/register.html', {'form': form, 'update_form': update_form})


class UserProfileView(DetailView):
    """
    View to display the user profile.

    Displays the profile of the currently logged-in user.
    """
    model = UserProfile
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def update_username(request):
    """
    View to handle updating the username.

    POST: Processes the form and updates the username.
    """
    if request.method == 'POST':
        form = UpdateUsernameForm(request.POST)

        if form.is_valid():
            new_username = form.cleaned_data['new_username']

            if User.objects.filter(username=new_username).exists():
                return render(request, 'users/update_username.html', {'form': form, 'error_message': 'Username already exists'})

            try:
                request.user.username = new_username
                request.user.save()
                return redirect('index')

            except IntegrityError:
                return render(request, 'users/update_username.html', {'form': form, 'error_message': 'Error updating username'})

    else:
        form = UpdateUsernameForm()

    return render(request, 'users/update_username.html', {'form': form})


@login_required
def update_profile_picture(request):
    """
    View to handle updating the profile picture.

    POST: Processes the form and updates the profile picture.
    """
    if request.method == 'POST':
        form = UpdateProfilePictureForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                profile_picture = form.cleaned_data['profile_picture']
                request.user.userprofile.profile_picture = profile_picture
                request.user.userprofile.save()
                return redirect('index')

            except IntegrityError:
                return render(request, 'users/update_profile_picture.html', {'form': form, 'error_message': 'Error updating profile picture'})

    else:
        form = UpdateProfilePictureForm()

    return render(request, 'users/update_profile_picture.html', {'form': form})
