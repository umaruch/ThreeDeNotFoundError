from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
# Create your models here.

"""Расширенная модель пользователя"""
class User(AbstractUser):
    profile_image = models.ImageField(verbose_name="Фото профиля",
                null=True,
                blank=True,
                upload_to="profile")

    description = models.TextField(verbose_name="Описание профиля", 
                max_length=256, 
                null=True, 
                blank=True)

"""Модель подписчиков"""
class Follower(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                verbose_name="Пользователь", 
                on_delete=models.CASCADE, 
                related_name="owner")
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL,
                verbose_name="Подписчик",  
                on_delete=models.CASCADE, 
                related_name="subscribers")

    def __str__(self):
        return f"Follower {self.subscriber} -> {self.user}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

"""Модель тэгов к моделям"""
class Tag(models.Model):
    name = models.CharField(verbose_name="Имя тэга", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        
"""Модель поста с 3Д моделью"""
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                verbose_name="Автор поста",
                on_delete=models.CASCADE,
                related_name="posts")
    preview_image = models.ImageField(verbose_name="Превью изображение",
                upload_to="post/preview")
    model_json = models.FileField(verbose_name='JSON 3dModel', 
                upload_to="post/model")
    description = models.TextField(verbose_name="Описание", 
                max_length=500, 
                null=True, 
                blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Набор тэгов", 
                related_name="posts")
    create_time = models.DateTimeField(verbose_name="Время создания", 
                auto_now_add=True, 
                blank=True)
    views_count = models.PositiveIntegerField(verbose_name="Количество просмотров", 
                blank=True, 
                default=0) 

    def __str__(self):
        return f"Post id:{self.id} by {self.author}"

    def get_tags(self):
        return "\n".join([tag.name for tag in self.tags.all()])

    class Meta:
        verbose_name = "Зд модель"
        verbose_name_plural = "3Д модели"
        ordering = ["create_time"]

"""Модель комментариев к постам"""
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                verbose_name="Автор комментария",
                on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                verbose_name="Пост",
                on_delete=models.CASCADE,
                related_name='comments')
    text = models.TextField(verbose_name="Текст комментария",
                max_length=500)
    create_time = models.DateTimeField(verbose_name="Время создания",
                blank=True,
                auto_now_add=True)

    def __str__(self):
        return f"Комментарий {self.author} к посту {self.post}"
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

        
