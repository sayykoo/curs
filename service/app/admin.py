from django.contrib import admin
from .models import CarServiceRequest, CustomUser, UserReviews, News, TeamMembers, ServicesPrice
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm
from django.utils.html import format_html

class CarServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_brand', 'problem_description', 'created_at', 'service_date', 'status')
    list_filter = ('status', 'service_date')
    search_fields = ('car_brand', 'user__username', 'problem_description')
    ordering = ('status', 'service_date')
    date_hierarchy = 'service_date' 

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    
    list_display = ('username', 'email', 'phone_number', 'avatar_preview', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'avatar', 'avatar_preview')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'avatar', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('avatar_preview',)
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "No avatar"
    avatar_preview.short_description = 'Preview'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CarServiceRequest, CarServiceRequestAdmin)
admin.site.register(UserReviews)
admin.site.register(News)
admin.site.register(TeamMembers)
admin.site.register(ServicesPrice)


