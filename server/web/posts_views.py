from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect

from .posts_services import get_posts_page, get_post, PostForm

"""Вьюха списка всех постов """
class PostsListView(View):
    def get(self, request):
        page_number = request.GET.get('page')
        return render(
            request,
            'index.html',
            {
                'title': "Главная",
                'posts': get_posts_page(page_number)
            }
        )

"""Подрбоный показ поста пользователю"""
class PostView(View):
    def get(self, request, post_id):
        post = get_post(post_id)
        form = CommentForm()
        post.views_count += 1
        post.save()
        return render(
            request,
            "post.html",
            {
                'title': f"Модель {post.author} №{post.id}",
                'post': post,
                'form': form
            }
        )

"""Создание нового поста"""    
class CreatePostView(View):
    def get(self, request):
        form = PostForm()
        return render(
            request,
            'base_form.html',
            {
                'title': "Создание нового поста",
                'form_url': '/posts/create',
                'form': form
            }
        )

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        for i in request.FILES:
            print(i)
        if form.is_valid():
            post = form.save(False)
            user = request.user
            post.author = user
            post.save()
            form.save_m2m()
            return redirect(f'/posts/{post.id}')
        return render(
            request,
            'base_form.html',
            {
                'title': "Создание нового поста",
                'form_url': '/posts/create',
                'form': form
            }
        )

"""Изменение выбранного поста"""
class ChangePostView(View):
    def get(self, request, post_id):
        post = get_post(post_id)
        if request.user == post.author:
            form = PostForm(instance=post)
            return render(
                request,
                'base_form.html',
                {
                    'title': "Редактирование поста",
                    'form_url': f'/posts/{post.id}/change',
                    'delete_url': f'/posts/{post.id}/delete',
                    'form': form
                }
            )

    def post(self, request, post_id):
        post = get_post(post_id)
        if request.user == post.author:
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect(f'/posts/{post.id}')
            return render(
                request,
                'base_form.html',
                {
                    'title': f"{post}",
                    'form_url': f'/posts/{post.id}/change',
                    'delete_url': f'/posts/{post.id}/delete',
                    'form': form
                }
            )

"""Удаление поста его хозяином"""
class DeletePostView(View):
    def post(self, request, post_id):
        post = get_post(post_id)
        # Если отославший запрос на удаление хозяин поста
        if post.author == request.user:
            post.delete()
            return redirect('/posts/')
