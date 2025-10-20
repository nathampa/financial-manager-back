# backend/transactions/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Receita'),
        ('EXPENSE', 'Despesa'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Usuário'
    )
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Conta'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.RESTRICT,
        related_name='transactions',
        verbose_name='Categoria'
    )
    description = models.CharField(max_length=255, verbose_name='Descrição')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor'
    )
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name='Tipo')
    date = models.DateField(verbose_name='Data')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['account']),
            models.Index(fields=['category']),
            models.Index(fields=['user', 'type']),
        ]

    def __str__(self):
        symbol = '+' if self.type == 'INCOME' else '-'
        return f"{symbol}R$ {self.amount} - {self.description}"

    def clean(self):
        """Validações customizadas"""
        if self.amount <= 0:
            raise ValidationError({'amount': 'O valor deve ser positivo.'})
        
        if self.date > timezone.now().date():
            raise ValidationError({'date': 'A data não pode ser futura.'})
        
        # Verifica se a categoria pertence ao usuário ou é do sistema
        if self.category.user and self.category.user != self.user:
            raise ValidationError({'category': 'Categoria inválida para este usuário.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)