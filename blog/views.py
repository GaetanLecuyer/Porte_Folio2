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

class Index(ListView):
    model = Article
    queryset = Article.objects.all().order_by('-date')
    template_name = 'blog/index.html'
    paginate_by = 2

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-date')
        category_filter = self.request.GET.get('category')
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_filter_form'] = CategoryFilterForm(initial={'category': self.request.GET.get('category')})

        # Vérifiez si l'utilisateur est connecté avant de créer le lien vers le profil utilisateur
        if self.request.user.is_authenticated:
            context['user_profile_url'] = reverse('user_profile', kwargs={'pk': self.request.user.pk})

        return context

class Featured(ListView):
	model = Article
	queryset = Article.objects.filter(featured=True).order_by('-date')
	template_name = 'blog/featured.html'
	paginate_by = 1

class DetailArticleView(DetailView, FormMixin):
    model = Article
    template_name = 'blog/blog_post.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context['liked_by_user'] = article.likes.filter(pk=self.request.user.id).exists()
        comments = Comment.objects.filter(article=article)
        context['comments'] = comments
        context['comment_form'] = CommentForm()  # Ajoutez ceci pour initialiser le formulaire
        return context

    def post(self, request, *args, **kwargs):
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
        return reverse('detail_article', kwargs={'pk': self.object.pk})
    
class LikeArticle(View):
	def post(self, request, pk):
		article = Article.objects.get(id=pk)
		if article.likes.filter(pk=self.request.user.id).exists():
			article.likes.remove(request.user.id)
		else:
			article.likes.add(request.user.id)

		article.save()
		return redirect('detail_article', pk)

class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Article
	template_name = 'blog/blog_delete.html'
	success_url = reverse_lazy('index')

	def test_func(self):
		article = Article.objects.get(id=self.kwargs.get('pk'))
		return self.request.user.id == article.author.id
	
class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content', 'category', 'featured', 'image']  # Liste des champs que vous souhaitez afficher
    template_name = 'blog/create_article.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SearchArticlesView(ListView):
    model = Article
    template_name = 'blog/search_articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        else:
            return Article.objects.all()

