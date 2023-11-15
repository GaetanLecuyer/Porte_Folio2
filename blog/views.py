# views.py

# Import necessary modules from Django
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Article, Comment, Category
from .forms import ArticleForm, CommentForm, CategoryFilterForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.db.models import Q

# Define the views for the 'blog' app


class Index(ListView):
    """
    Display a paginated list of articles on the index page.

    The index page includes a category filter form to filter articles by category.

    Attributes:
        model (Article): The model to use for the list view.
        queryset (QuerySet): The queryset to fetch articles from the database.
        template_name (str): The name of the template to render.
        paginate_by (int): The number of articles to display per page.

    Methods:
        get_queryset: Get the queryset of articles, applying category filtering if specified.
        get_context_data: Get the context data to pass to the template.

    """

    model = Article
    queryset = Article.objects.all().order_by('-date')
    template_name = 'blog/index.html'
    paginate_by = 2

    def get_queryset(self):
        """
        Get the queryset of articles, applying category filtering if specified.

        Returns:
            QuerySet: The queryset of articles to display.

        """
        queryset = Article.objects.all().order_by('-date')
        category_filter = self.request.GET.get('category')
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context data to pass to the template.

        Returns:
            dict: The context data.

        """
        context = super().get_context_data(**kwargs)
        context['category_filter_form'] = CategoryFilterForm(
            initial={'category': self.request.GET.get('category')})

        # Check if the user is authenticated before creating the link to the user profile
        if self.request.user.is_authenticated:
            context['user_profile_url'] = reverse(
                'user_profile', kwargs={'pk': self.request.user.pk})

        return context


class Featured(ListView):
    """
    Display a paginated list of featured articles.

    Attributes:
        model (Article): The model to use for the list view.
        queryset (QuerySet): The queryset to fetch featured articles from the database.
        template_name (str): The name of the template to render.
        paginate_by (int): The number of articles to display per page.

    """

    model = Article
    queryset = Article.objects.filter(featured=True).order_by('-date')
    template_name = 'blog/featured.html'
    paginate_by = 1


class DetailArticleView(DetailView, FormMixin):
    """
    Display the details of a specific article, including comments.

    Users can like the article and leave comments.

    Attributes:
        model (Article): The model to use for the detail view.
        template_name (str): The name of the template to render.
        form_class (CommentForm): The form class for handling comments.

    Methods:
        get_context_data: Get the context data to pass to the template.
        post: Handle POST requests, allowing users to leave comments.
        get_success_url: Get the URL to redirect to after a successful form submission.

    """

    model = Article
    template_name = 'blog/blog_post.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        """
        Get the context data to pass to the template.

        Returns:
            dict: The context data.

        """
        context = super().get_context_data(**kwargs)
        article = self.object
        context['liked_by_user'] = article.likes.filter(
            pk=self.request.user.id).exists()
        comments = Comment.objects.filter(article=article)
        context['comments'] = comments
        # Add this to initialize the form
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests, allowing users to leave comments.

        Returns:
            HttpResponse: The response after processing the form submission.

        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = self.request.user
            new_comment.article = self.object
            new_comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """
        Get the URL to redirect to after a successful form submission.

        Returns:
            str: The success URL.

        """
        return reverse('detail_article', kwargs={'pk': self.object.pk})


class LikeArticle(View):
    """
    Handle user likes on an article.

    Users can like or unlike an article.

    Attributes:
        None

    Methods:
        post: Handle POST requests, allowing users to like or unlike an article.

    """

    def post(self, request, pk):
        """
        Handle POST requests, allowing users to like or unlike an article.

        Returns:
            HttpResponse: The response after processing the like action.

        """
        article = Article.objects.get(id=pk)
        if article.likes.filter(pk=self.request.user.id).exists():
            article.likes.remove(request.user.id)
        else:
            article.likes.add(request.user.id)

        article.save()
        return redirect('detail_article', pk)


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow the author to delete their own article.

    Attributes:
        model (Article): The model to use for the delete view.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after a successful deletion.

    Methods:
        test_func: Check if the user is the author of the article.

    """

    model = Article
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        """
        Check if the user is the author of the article.

        Returns:
            bool: True if the user is the author, False otherwise.

        """
        article = Article.objects.get(id=self.kwargs.get('pk'))
        return self.request.user.id == article.author.id


class CreateArticleView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create a new article.

    Attributes:
        model (Article): The model to use for the create view.
        fields (list): The list of fields to display in the create form.
        template_name (str): The name of the template to render.
        success_url (str): The URL to redirect to after a successful article creation.

    Methods:
        form_valid: Set the author of the article before saving the form.

    """

    model = Article
    fields = ['title', 'content', 'category', 'featured',
              'image']  # List of fields you want to display
    template_name = 'blog/create_article.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        Set the author of the article before saving the form.

        Returns:
            HttpResponse: The response after processing the form submission.

        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class SearchArticlesView(ListView):
    """
    Display search results for articles.

    Attributes:
        model (Article): The model to use for the list view.
        template_name (str): The name of the template to render.
        context_object_name (str): The name to use for the context object in the template.
        paginate_by (int): The number of articles to display per page.

    Methods:
        get_queryset: Get the queryset of articles based on the search query.

    """

    model = Article
    template_name = 'blog/search_articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        """
        Get the queryset of articles based on the search query.

        Returns:
            QuerySet: The queryset of articles to display.

        """
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        else:
            return Article.objects.all()
