# apps/properties/admin.py
from django.contrib import admin
from .models import Property, PropertyImage, PropertySearch

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'price', 'city', 'advert_type', 'published_status']
    list_filter = ['advert_type', 'property_type', 'city', 'published_status']
    search_fields = ['title', 'city', 'description']
    inlines = [PropertyImageInline]

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertySearch)