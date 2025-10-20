# backend/categories/management/commands/create_default_categories.py
# Crie a estrutura: categories/management/commands/create_default_categories.py

from django.core.management.base import BaseCommand
from categories.models import Category


class Command(BaseCommand):
    help = 'Cria categorias padrão do sistema'

    def handle(self, *args, **kwargs):
        default_categories = [
            # Receitas
            {'name': 'Salário', 'type': 'INCOME', 'icon': '💼'},
            {'name': 'Freelance', 'type': 'INCOME', 'icon': '💻'},
            {'name': 'Investimentos', 'type': 'INCOME', 'icon': '📈'},
            {'name': 'Prêmios', 'type': 'INCOME', 'icon': '🎁'},
            {'name': 'Outros', 'type': 'INCOME', 'icon': '💰'},
            
            # Despesas
            {'name': 'Alimentação', 'type': 'EXPENSE', 'icon': '🍔'},
            {'name': 'Transporte', 'type': 'EXPENSE', 'icon': '🚗'},
            {'name': 'Moradia', 'type': 'EXPENSE', 'icon': '🏠'},
            {'name': 'Saúde', 'type': 'EXPENSE', 'icon': '🏥'},
            {'name': 'Educação', 'type': 'EXPENSE', 'icon': '📚'},
            {'name': 'Lazer', 'type': 'EXPENSE', 'icon': '🎮'},
            {'name': 'Vestuário', 'type': 'EXPENSE', 'icon': '👕'},
            {'name': 'Beleza', 'type': 'EXPENSE', 'icon': '💄'},
            {'name': 'Pets', 'type': 'EXPENSE', 'icon': '🐶'},
            {'name': 'Contas', 'type': 'EXPENSE', 'icon': '📄'},
            {'name': 'Outros', 'type': 'EXPENSE', 'icon': '💸'},
        ]

        created_count = 0
        for cat_data in default_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                type=cat_data['type'],
                user=None,  # Categoria do sistema
                defaults={'icon': cat_data['icon']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Categoria criada: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Categoria já existe: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n{created_count} categorias criadas com sucesso!')
        )