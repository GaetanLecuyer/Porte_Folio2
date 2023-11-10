from django.urls import path, include
from .views import Index
from .views import Index, DetailArticleView, LikeArticle, Featured, DeleteArticleView
from .views import CreateArticleView, SearchArticlesView
from django.conf import settings
from django.conf.urls.static import static
from users.views import UserProfileView, update_username, update_profile_picture

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', Index.as_view(), name='index'),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article'),
    path('<int:pk>/like', LikeArticle.as_view(), name='like_article'),
    path('featured/', Featured.as_view(), name='featured'),
    path('<int:pk>/delete', DeleteArticleView.as_view(), name='delete_article'),
    path('create/', CreateArticleView.as_view(), name='create_article'),
    path('search/', SearchArticlesView.as_view(), name='search_articles'),
    path('accounts/profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('accounts/profile/update-username/', update_username, name='update_username'),
    path('accounts/profile/update-profile-picture/', update_profile_picture, name='update_profile_picture'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
