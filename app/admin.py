from django.contrib import admin
from .models import Category, Event

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'time', 'is_active')
    list_filter = ('category', 'date', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}