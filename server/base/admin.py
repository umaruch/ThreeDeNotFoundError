from django.contrib import admin

from .models import User, Follower, Tag, Post, Comment

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'last_login', 'date_joined']
    list_display_links = ['username', 'email']
    search_fields = ['username', 'email']
    list_filter = ['is_staff']
    sortable_by = ['last_login', 'date_joined']

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscriber']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'create_time', 'get_tags', 'views_count')
    readonly_fields = ('author', 'create_time', 'views_count')

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.author = request.user
        obj.save()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'create_time']
    search_fields = ['author', 'post']
    sortable_by = ['create_time']