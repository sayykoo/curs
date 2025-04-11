from django.contrib import admin
from .models import CarServiceRequest

@admin.register(CarServiceRequest)
class CarServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user' ,'name', 'phone', 'car_brand', 'created_at', 'problem_description', 'service_date', 'status')
    list_filter = ('created_at', 'car_brand')
    search_fields = ('name', 'phone', 'car_brand')