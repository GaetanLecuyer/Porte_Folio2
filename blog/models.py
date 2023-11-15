# models.py

# Import necessary modules from Django and third-party libraries
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Define a function to set the default image for an Article


def default_image():
    return "article_images/default_image.jpg"

# Define a Category model


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Define an Article model


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    image = models.ImageField(
        upload_to='article_images/', default=default_image)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

# Define a Comment model


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
