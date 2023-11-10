from django.db import models
from django.contrib.auth.models import User
import os

def user_directory_path(instance, filename):
    # Obtenez le nom d'utilisateur de l'instance
    username = instance.user.username

    # Déterminez l'emplacement où la photo de profil sera enregistrée
    directory_path = f'profile_pictures/user_{username}/'

    # Assurez-vous que le répertoire existe, sinon, créez-le
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    return f'{directory_path}{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return self.user.username
