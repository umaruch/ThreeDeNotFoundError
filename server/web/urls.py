from django.urls import path
from django.views.generic.base import RedirectView

from .views import RegisterView, LoginView, LogoutView, UserProfileView, PostsListView, PostView

urlpatterns = [
    # Авторизация
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    # Операции с пользователями
    path('users/<int:user_id>', UserProfileView.as_view(), name="user"),
    #path('users/edit',)
    # Операции с постами
    path('', RedirectView.as_view(url="/posts/", permanent=True)),
    path('posts/', PostsListView.as_view()),
    path('posts/<int:post_id>', PostView.as_view())
    # Дополнительное
]