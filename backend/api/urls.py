"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import SignupView, login_view, get_user_profile, get_articles, UpdateFavoriteTopicView, UpdateUserEmailView, UpdateUserDateOfBirthView,UpdateUserProfilePictureView, CommentCreateView, UpdateArticleCommentsView
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('registration_success/', TemplateView.as_view(template_name='registration/registration_success.html'), name='registration_success'),
    path('login/', login_view, name='login'),
    path('get_user_profile/', get_user_profile, name='get_user_profile'),
    path('get_articles/', get_articles, name='get_articles'),
    path('update_favorite_topic/', UpdateFavoriteTopicView.as_view(), name='update_favorite_topic'),
    path('update_user_email/', UpdateUserEmailView.as_view(), name='update_user_email'),
    path('update_user_date_of_birth/', UpdateUserDateOfBirthView.as_view(), name='update_user_date_of_birth'),
    path('update_user_profile_picture/', UpdateUserProfilePictureView.as_view(), name='update_user_profile_picture'),
    path('update_article_comments/', UpdateArticleCommentsView.as_view(), name='update_article_comments'),

]
