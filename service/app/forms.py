from django import forms
from .models import CarServiceRequest, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

class CarServiceForm(forms.ModelForm):
    class Meta:
        model = CarServiceRequest
        fields = ['name', 'phone', 'car_brand']

class SignUpForm(UserCreationForm):
    # name = forms.EmailField(max_length=30, help_text='Обязательное поле. Введите ваше имя.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'avatar')