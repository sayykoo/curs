from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit-form/', views.submit_form, name='submit_form'),
    path('login/', views.login_view, name='login'),
    path('register/', views.signup_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('about_company/', views.about_company, name='about'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('reviews/', views.reviews, name='reviews'),
    path('add-review/', views.add_review, name='add_review'),
    path('toggle-review/<int:review_id>/', views.toggle_review, name='toggle_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('news/', views.news_page, name='news_page'),
    path('news/delete/<int:news_id>/', views.delete_news, name='delete_news'),
    path('news/<int:news_id>/edit/', views.update_news, name='update_news'),
    path('news/add/', views.add_news, name='add_news'),
    path('contacts/', views.contacts_page, name='contacts'),
    path('services/', views.services_price, name='services'),
]
