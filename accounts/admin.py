# backend/accounts/admin.py
from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'type', 'initial_balance', 'current_balance', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name', 'user__email']
    readonly_fields = ['id', 'created_at']
    
    def current_balance(self, obj):
        return f"R$ {obj.current_balance:.2f}"
    current_balance.short_description = 'Saldo Atual'