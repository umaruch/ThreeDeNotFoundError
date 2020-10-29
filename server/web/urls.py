from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

from .views import RegisterView, LoginView, LogoutView, UserProfileView, PostsListView, PostView, UserChangeView, CreatePostView

urlpatterns = [
    # Авторизация
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    # Операции с пользователями
    path('users/<int:user_id>', UserProfileView.as_view()),
    path('users/edit', login_required(UserChangeView.as_view())),
    # Операции с постами
    path('', RedirectView.as_view(url="/posts/", permanent=True)),
    path('posts/', PostsListView.as_view()),
    path('posts/<int:post_id>', PostView.as_view()),
    path('posts/create', login_required(CreatePostView.as_view())),
    # Дополнительное
]