# backend/accounts/models.py
from django.db import models
from django.conf import settings
import uuid

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CHECKING', 'Conta Corrente'),
        ('SAVINGS', 'Poupança'),
        ('CREDIT_CARD', 'Cartão de Crédito'),
        ('CASH', 'Dinheiro'),
        ('INVESTMENT', 'Investimentos'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='Usuário'
    )
    name = models.CharField(max_length=100, verbose_name='Nome')
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, verbose_name='Tipo')
    initial_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Saldo Inicial'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    @property
    def current_balance(self):
        """Calcula o saldo atual da conta"""
        from transactions.models import Transaction
        
        income = Transaction.objects.filter(
            account=self,
            type='INCOME'
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        expense = Transaction.objects.filter(
            account=self,
            type='EXPENSE'
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        return self.initial_balance + income - expense