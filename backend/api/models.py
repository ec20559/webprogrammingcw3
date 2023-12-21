# backend/api/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    favorite_topic = models.CharField(max_length=75, default=None, blank=True, null=True)
    # Added related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        related_query_name='custom_user_group',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        related_query_name='custom_user_permission',
        blank=True,
    )

    def __str__(self):
        return self.username

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey('NewsArticle', related_name='article_comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} - {self.article.title} Comment'

class NewsArticle(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    topic = models.CharField(max_length=100)
    contents = models.TextField()

    comments = models.ManyToManyField('Comment', related_name='comments_on_article', blank=True)
