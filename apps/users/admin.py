# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'is_agent', 'is_staff', 'date_joined']
    list_filter = ['is_agent', 'is_staff']
    search_fields = ['email', 'full_name']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'city', 'address', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_agent')}),
    )

admin.site.register(User, UserAdmin)