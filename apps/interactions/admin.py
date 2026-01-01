# apps/interactions/admin.py
from django.contrib import admin
from .models import PropertyInspection, Message, Announcement

class PropertyInspectionAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'agent', 'inspection_date', 'status']
    list_filter = ['status', 'inspection_date']

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']

admin.site.register(PropertyInspection, PropertyInspectionAdmin)
admin.site.register(Message)
admin.site.register(Announcement, AnnouncementAdmin)