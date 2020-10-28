from django.core.paginator import Paginator
from django.conf import settings

from base.models import Post

"""Получение страницы с постами"""
def get_posts_page(page):
    posts_list = Post.objects.all()
    posts_pages = Paginator(posts_list, settings.PAGINATE_BY)
    return posts_pages.get_page(page)

"""Получение определенного поста по id в БД"""
def get_post(post_id):
    post = Post.objects.get(id=post_id)
    return post

