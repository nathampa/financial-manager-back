# backend/categories/models.py
from django.db import models
from django.conf import settings
import uuid

class Category(models.Model):
    CATEGORY_TYPES = [
        ('INCOME', 'Receita'),
        ('EXPENSE', 'Despesa'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Usuário',
        null=True,
        blank=True,
        help_text='Deixe em branco para categorias padrão do sistema'
    )
    name = models.CharField(max_length=100, verbose_name='Nome')
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES, verbose_name='Tipo')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Ícone')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        prefix = "Sistema" if self.user is None else f"Usuário {self.user.email}"
        return f"{self.name} ({prefix})"