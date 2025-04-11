from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .forms import CarServiceForm, LoginForm, SignUpForm
from .models import CarServiceRequest, CustomUser
from django.contrib.auth import login, authenticate

def index(request):
    return render(request, 'app/index.html')

class Login(LoginView):
    template_name = 'accounts/login.html' 

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'auth/login.html', {'form': form})

@login_required
def submit_form(request):
    if request.method == 'POST':
        form = CarServiceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.user = request.user
            instance.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect('index')
    else:
        form = CarServiceForm()
    
    return render(request, 'app/templates/entry_form.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.userprofile
    user_requests = CarServiceRequest.objects.filter(user=request.user).select_related('user')
    profile, created = CustomUser.objects.get_or_create(user=request.user)

    context = {
        'profile': profile,
        'user_requests': request.user,
    }
    return render(request, 'auth/profile.html', context)

