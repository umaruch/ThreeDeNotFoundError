from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from .user_forms import RegisterNewUser, LoginUser

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
            return render(
                request,
                'test.html'
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
                return render(
                    request,
                    'test.html'
                )
