# backend/transactions/admin.py
from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'account', 'category', 'amount', 'type', 'date']
    list_filter = ['type', 'date', 'category']
    search_fields = ['description', 'user__email']
    date_hierarchy = 'date'
    readonly_fields = ['id', 'created_at']