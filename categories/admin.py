# backend/categories/admin.py
from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'user', 'icon']
    list_filter = ['type']
    search_fields = ['name', 'user__email']