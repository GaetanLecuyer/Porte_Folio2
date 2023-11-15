# forms.py

# Import necessary modules from Django
from django import forms
from .models import Article, Comment, Category
from widget_tweaks.templatetags.widget_tweaks import *

# Define a form for creating or updating an Article


class ArticleForm(forms.ModelForm):
    # Define the 'category' field as a ModelChoiceField with a queryset of all Category objects
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Select a category")

    class Meta:
        # Set the model to Article and include specific fields
        model = Article
        fields = ['title', 'content', 'category', 'featured', 'image']
        # Define widgets to customize the appearance of form fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Define a form for adding comments to an Article


class CommentForm(forms.ModelForm):
    class Meta:
        # Set the model to Comment
        model = Comment
        # Include the 'content' field for user input
        fields = ['content']
        # Define a widget to customize the appearance of the comment content field
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment...'}),
        }

# Define a form for filtering Articles based on category


class CategoryFilterForm(forms.Form):
    # Define the 'category' field as a ModelChoiceField with a queryset of all Category objects
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="All Categories", required=False)
