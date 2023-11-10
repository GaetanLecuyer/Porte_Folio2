from django import forms
from .models import Article, Comment, Category
from widget_tweaks.templatetags.widget_tweaks import *

class ArticleForm(forms.ModelForm):
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category")

    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'featured', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Assurez-vous que le modèle Comment est importé
        fields = ['content']  # Ajoutez les champs dont vous avez besoin pour les commentaires
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment...'}),
        }

class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="All Categories", required=False)