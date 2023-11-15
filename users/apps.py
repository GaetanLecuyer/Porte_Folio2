# apps.py in the 'users' app

from django.apps import AppConfig


class UsersConfig(AppConfig):
    # Set the default auto field for model primary keys to BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'

    # Set the name of the app to 'users'
    name = 'users'
