from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .forms import CarServiceForm, LoginForm, SignUpForm, ReviewForm, NewsForm
from .models import CarServiceRequest, CustomUser, UserProfile, UserReviews, News, TeamMembers, ServicesPrice
from django.contrib.auth import login, authenticate
import logging


logger = logging.getLogger(__name__)

def index(request):
    members = TeamMembers.objects.all()

    context = {
        'members': members
    }

    return render(request, 'app/index.html', context)


def about_company(request):
    return render(request, 'app/about_company.html')


def news_page(request):
    posts = News.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'app/news.html', context)


@staff_member_required
def delete_news(request, news_id):
    if request.method == 'POST' and request.user.is_staff:
        news = get_object_or_404(News, id=news_id)
        news.delete()
    return redirect('news_page')


@staff_member_required
def update_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_page')
    else:
        form = NewsForm(instance=news)
    return render(request, 'app/edit_news.html', {'form': form, 'news': news})

def signup_view(request):
    if request.method == 'POST':
        logger.info(f"Получены данные формы: {request.POST}")
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                logger.info(f"Создан пользователь: {user.username}")
                login(request, user)
                return redirect('index')
            except Exception as e:
                logger.error(f"Ошибка при создании пользователя: {e}")
        else:
            logger.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = SignUpForm()
    
    return render(request, 'auth/register.html', {'form': form})


def contacts_page(request):
    return render(request, 'app/contacts_page.html')

def services_price(request):
    price = ServicesPrice.objects.all()

    context = {
        'price': price,
        'title': 'SpeedyMech'
    }

    return render(request, 'app/services.html', context)

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    return render(request, 'auth/login.html', {'form': form})



def reviews(request): #отображение отзывов
    users_reviews = UserReviews.objects.filter(is_published=True).order_by('-created_at')
    
    if request.user.is_staff:
        users_reviews = UserReviews.objects.all().order_by('-created_at')
    
    context = {
        'users_reviews': users_reviews
    }
    return render(request, 'app/reviews.html', context)



@login_required
def add_review(request): #добавление отзыва
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'app/add_review.html', {'form': form})


@staff_member_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('news_page')
    else:
        form = NewsForm(user=request.user)
    
    return render(request, 'app/new_add.html', {'form': form})


@staff_member_required
def toggle_review(request, review_id): 
    review = UserReviews.objects.get(id=review_id)
    review.is_published = not review.is_published
    review.save()
    return redirect('reviews')



@staff_member_required
def delete_review(request, review_id): #удаление отзыва
    review = UserReviews.objects.get(id=review_id)
    review.delete()
    return redirect('reviews')



@login_required
def help_submit(request): #заявка помощи
    if request.method == 'POST':
        form = CarServiceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.user = request.user
            instance.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))
    else:
        form = CarServiceForm()



@login_required 
def submit_form(request): #форма отправки заявки
    if request.method == 'POST':
        form = CarServiceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, '✅ Ваша заявка успешно отправлена!')
            return redirect('index')
        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CarServiceForm()
    
    return redirect('index')



@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.user.is_staff:
        service_requests = CarServiceRequest.objects.all().order_by('-created_at')
    else:
        service_requests = CarServiceRequest.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'profile': profile,
        'user': request.user,
        'service_requests': service_requests
    }
    return render(request, 'auth/profile.html', context)


