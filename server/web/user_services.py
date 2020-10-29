from django import forms

from django.conf import settings
from base.models import User


"""Форма регистрация пользователя"""
class RegisterNewUser(forms.Form):
    username = forms.CharField(max_length=32, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)

    """Проверка на наличие такого-же имени пользователя"""
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    """Проверка наличия email"""
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    """Проверка совпадения паролей"""
    def clean_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']
        if len(password1)<settings.PASSWORD_LEN:
            raise forms.ValidationError('Password short')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
            
        return password1

    """Создание нового пользователя"""
    def save(self):
        form_data = self.cleaned_data
        user = User.objects.create(username=form_data['username'], email=form_data['email'])
        user.set_password(form_data['password'])
        user.save()
        return user

"""Форма входа пользователей"""
class LoginUser(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)

    def get_user(self):
        form_data = self.cleaned_data
        try:
            user = User.objects.get(email=form_data['email'])
            if user:
                if user.check_password(form_data['password']):
                    return user
                raise forms.ValidationError("Password incorrect")
            else:
                raise forms.ValidationError("User not found")
        except User.DoesNotExist:
            return None

"""Форма изменения данных пользователя"""
class ChangeUserInfo(forms.Form):
    user_id = None
    user = None
    profile_image = forms.ImageField(required=False)
    username = forms.CharField(
        max_length=32,
        required=True
    )
    email = forms.EmailField(required=True)
    description = forms.CharField(required=False,
        max_length=256,
        widget=forms.Textarea)
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput
    )

    """Проверка на наличие такого-же имени пользователя"""
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    """Проверка наличия email"""
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    """Проверка совпадения паролей"""
    # def clean_password(self):
    #     password = self.cleaned_data['current_password']
    #     self.user = User.objects.get(id=self.user_id)
    #     if self.user.check_password(password):
    #         return password
    #     else:
    #         raise forms.ValidationError("Password incorrect")

    def save(self):
        self.user = User.objects.get(id=self.user_id)
        data = self.cleaned_data
        self.user.username = data.get('username')
        self.user.email = data.get('email')
        self.user.description = data.get('description')
        self.profile_image = data.get('profile_image')
        self.user.save()
        # self.user.set_password(data.)
        

"""Получение обьекта пользователя по его id"""
def get_user(user_id):
    user = User.objects.get(id=user_id)
    return user