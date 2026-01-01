# apps/profiles/admin.py
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'is_agent']
    list_filter = ['is_agent', 'city']
    search_fields = ['user__email', 'phone_number']

admin.site.register(Profile, ProfileAdmin)