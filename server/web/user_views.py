from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .user_services import RegisterNewUser, LoginUser, ChangeUserInfo, get_user

"""Вьюха регистрации нового пользователя"""
class RegisterView(View):
    """Отправка формы"""
    def get(self, request):
        form = RegisterNewUser()
        return render(
            request,
            'auth_base_form.html',
            {
                'title': 'Регистрация',
                'form_url': '/register/',
                'form': form
            }
        )

    """Обработка полученной запоненной(надеюсь) формы"""
    def post(self, request):
        form = RegisterNewUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/posts/')

        return render(
            request,
            'auth_base_form.html',
            {
                'title': 'Регистрация',
                'form_url': '/register/',
                'form': form
            }
        )

"""Вьюха входа пользователя"""
class LoginView(View):
    def get(self, request):
        form = LoginUser()
        return render(
            request,
            'auth_base_form.html',
            {
                'title': 'Вход',
                'form_url': '/login/',
                'form': form
            }
        )

    def post(self, request):
        form = LoginUser(request.POST)
        if form.is_valid():
            print("Форма прошла проверку")
            user = form.get_user()
            if user:
                print("Пользователь найден")
                login(request, user)
                return redirect('/posts/')

        return render(
            request,
            'auth_base_form.html',
            {
                'title': 'Вход',
                'form_url': '/login/',
                'form': form
            }
        )

"""Выход текущего пользователя"""
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/posts/')

"""Вьюха профиля пользователя"""
class UserProfileView(View):
    def get(self, request, user_id):
        user = get_user(user_id)
        return render(
            request,
            'profile.html',
            {
                'title': f"Профиль {user.username}",
                'profile': user
            }
        )

class UserChangeView(View):
    def get(self, request):
        form = ChangeUserInfo(
            initial={
                'profile_image': request.user.profile_image.url,
                'username': request.user.username,
                'email': request.user.email,
                'description': request.user.description
            }
        )
        return render(
            request,
            'base_form.html',
            {
                'title': 'Изменение профиля пользователя',
                'form_url': '/users/edit',
                'form': form
            }
        )

    def post(self, request):
        form = ChangeUserInfo(request.POST)
        form.user_id = request.user.id
        if form.is_valid():
            form.save()
            return redirect(
                f'/users/{request.user.id}'
            )
        return render(
            request,
            'base_form.html',
            {
                'title': 'Изменение профиля пользователя',
                'form_url': '/users/edit',
                'form': form
            }
        )