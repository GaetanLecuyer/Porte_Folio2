from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UpdateUsernameForm, UpdateProfilePictureForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse 
from django.db import IntegrityError

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        update_form = UpdateProfilePictureForm()
        return render(request, 'users/register.html', {'form': form, 'update_form': update_form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        update_form = UpdateProfilePictureForm(request.POST, request.FILES)

        if form.is_valid() and update_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Assurez-vous de définir correctement le mot de passe
            user.save()

            profile_picture = update_form.cleaned_data['profile_picture']

            # Vérifiez si le profil utilisateur existe pour l'utilisateur actuel
            if hasattr(user, 'userprofile'):
                user.userprofile.profile_picture = profile_picture
            else:
                # Créez le profil utilisateur s'il n'existe pas
                UserProfile.objects.create(user=user, profile_picture=profile_picture)

            # Enregistrez l'utilisateur et le profil utilisateur
            user.save()
            user.userprofile.save()

            return redirect('index')  # Redirige vers la vue nommée 'index'

        else:
            # Gérez le cas où l'un des formulaires n'est pas valide
            return render(request, 'users/register.html', {'form': form, 'update_form': update_form})
             
class UserProfileView(DetailView):
    model = UserProfile  # Changez le modèle pour UserProfile au lieu de User
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@login_required
def update_username(request):
    if request.method == 'POST':
        form = UpdateUsernameForm(request.POST)

        if form.is_valid():
            new_username = form.cleaned_data['new_username']

            # Vérifiez si le nouveau nom d'utilisateur existe déjà
            if User.objects.filter(username=new_username).exists():
                return render(request, 'users/update_username.html', {'form': form, 'error_message': 'Username already exists'})

            try:
                # Changez le nom d'utilisateur
                request.user.username = new_username
                request.user.save()

                # Redirigez vers la page d'accueil
                return redirect('index')

            except IntegrityError:
                return render(request, 'users/update_username.html', {'form': form, 'error_message': 'Error updating username'})

    else:
        form = UpdateUsernameForm()

    return render(request, 'users/update_username.html', {'form': form})

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = UpdateProfilePictureForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Traitez la photo de profil
                profile_picture = form.cleaned_data['profile_picture']
                request.user.userprofile.profile_picture = profile_picture
                request.user.userprofile.save()

                # Redirigez vers la page d'accueil
                return redirect('index')

            except IntegrityError:
                return render(request, 'users/update_profile_picture.html', {'form': form, 'error_message': 'Error updating profile picture'})

    else:
        form = UpdateProfilePictureForm()

    return render(request, 'users/update_profile_picture.html', {'form': form})