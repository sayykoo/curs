from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
    

class ServicesPrice(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название работы')
    price = models.CharField(max_length=100, verbose_name='Цена')
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title

class TeamMembers(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    type = models.CharField(max_length=50, verbose_name='Тип работы')
    image = models.ImageField(upload_to='member_images/', verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return self.name
    

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение', blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class UserReviews(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="userprofile"
    )

    def __str__(self):
        return f"Профиль {self.user.username}"


class CarServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("completed", "Завершена"),
        ("canceled", "Отменена"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    car_brand = models.CharField(max_length=50, verbose_name="Марка автомобиля")
    problem_description = models.TextField(
        verbose_name="Описание проблемы", null=True, default="Не указано"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    service_date = models.DateField(
        verbose_name="Дата обслуживания", null=True, blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    class Meta:
        verbose_name = "Заявка на сервис"
        verbose_name_plural = "Заявки на сервис"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка #{self.id} - {self.car_brand} ({self.get_status_display()})"
