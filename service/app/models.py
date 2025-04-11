from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CarServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    car_brand = models.CharField(max_length=50, verbose_name='Марка автомобиля')
    problem_description = models.TextField(max_length=100, verbose_name='Описание проблемы', null=True, default='Не указано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    service_date = models.DateField(verbose_name='Дата обслуживания', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    

    class Meta:
        verbose_name = 'Заявка на сервис'
        verbose_name_plural = 'Заявки на сервис'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{self.id} - {self.car_brand} ({self.get_status_display()})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating profile for {instance.username}")
        UserProfile.objects.create(user=instance)


