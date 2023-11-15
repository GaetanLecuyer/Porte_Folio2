# admin.py

# Import necessary modules from Django
from django.contrib import admin

# Import models from the current application
from .models import Article, Category

# Register Article and Category models with the admin site
admin.site.register(Article)
admin.site.register(Category)
