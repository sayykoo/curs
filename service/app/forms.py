from django import forms
from .models import CarServiceRequest
from django.contrib.auth.forms import UserCreationForm

class CarServiceForm(forms.ModelForm):
    class Meta:
        model = CarServiceRequest
        fields = ['name', 'phone', 'car_brand']

class RegisterForm(UserCreationForm):
    class Meta:
        fields = ['username', 'password1', 'password2']