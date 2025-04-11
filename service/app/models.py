from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

class CarServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    car_brand = models.CharField(max_length=50, verbose_name='Марка автомобиля')
    problem_description = models.TextField(verbose_name='Описание проблемы', null=True, default='Не указано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    service_date = models.DateField(verbose_name='Дата обслуживания', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    

    class Meta:
        verbose_name = 'Заявка на сервис'
        verbose_name_plural = 'Заявки на сервис'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{self.id} - {self.car_brand} ({self.get_status_display()})"



