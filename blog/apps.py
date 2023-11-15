# apps.py

# Import AppConfig from Django
from django.apps import AppConfig

# Define a configuration class for the 'blog' app


class BlogConfig(AppConfig):
    # Set the default_auto_field to 'django.db.models.BigAutoField'
    default_auto_field = 'django.db.models.BigAutoField'
    # Set the name of the app to 'blog'
    name = 'blog'
