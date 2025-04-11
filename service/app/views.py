from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .forms import CarServiceForm
from .models import UserProfile, CarServiceRequest

def index(request):
    return render(request, 'app/index.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html' 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User created: {user.username}")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

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
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'profile': profile,
        'user_requests': user_requests,
    }
    return render(request, 'app/profile.html', context)

