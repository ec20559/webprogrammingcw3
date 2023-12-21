
# Register your models here.
from django.contrib import admin
from .models import CustomUser, NewsArticle

admin.site.register(CustomUser)
admin.site.register(NewsArticle)