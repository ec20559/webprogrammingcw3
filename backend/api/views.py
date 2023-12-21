from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import NewsArticle, Comment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from rest_framework import generics, serializers
from rest_framework.response import Response

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('registration_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('registration_success')
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})


def get_user_profile(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'date_of_birth': str(user.date_of_birth),
        'profile_image': user.profile_image.url if user.profile_image else None,
        'favorite_topic': user.favorite_topic if user.favorite_topic else "None",
    }
    response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response["Access-Control-Allow-Credentials"] = "true"
    return response


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'


@api_view(['GET'])
def get_articles(request):
    articles = NewsArticle.objects.all()
    serializer = NewsArticleSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe=False, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class UpdateFavoriteTopicView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            favorite_topic = data.get('favorite_topic')

            user = request.user
            user.favorite_topic = favorite_topic
            user.save()

            return JsonResponse({'success': 'Favorite topic updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserEmailView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')

            user = request.user
            user.email = email
            user.save()

            return JsonResponse({'success': 'Email updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserDateOfBirthView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            date_of_birth = data.get('date_of_birth')

            user = request.user
            user.date_of_birth = date_of_birth
            user.save()

            return JsonResponse({'success': 'Date of Birth updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserProfilePictureView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            profile_image = data.get('profile_image')

            user = request.user
            user.profile_image = profile_image
            user.save()

            return JsonResponse({'success': 'Profile Picture updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'author', 'article']


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'article']


class CommentListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article_id=article_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentListSerializer


class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            article_id = kwargs.get('article_id')
            text = request.POST.get('text')  


            comment = Comment.objects.create(text=text, article_id=article_id, author=request.user)


            comments = Comment.objects.filter(article_id=article_id).values('id', 'text', 'author__username')

            return JsonResponse({'success': 'Comment created successfully', 'comments': list(comments)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class ArticleDetailView(View):
    template_name = 'article_detail.html'

    def get(self, request, *args, **kwargs):
        article_id = kwargs['article_id']
        article = NewsArticle.objects.get(id=article_id)
        comments = Comment.objects.filter(article=article)

        context = {'article': article, 'comments': comments}
        return render(request, self.template_name, context)

class UpdateArticleCommentsView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            article_id = data.get('articleId')
            comments = data.get('comments')

            article = NewsArticle.objects.get(id=article_id)
            article.comments = comments
            article.save()

            return JsonResponse({'success': 'Comments updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)