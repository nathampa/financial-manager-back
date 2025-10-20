# backend/transactions/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction
from .serializers import TransactionSerializer, TransactionListSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """CRUD completo de transações"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TransactionListSerializer
        return TransactionSerializer
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filtros por query params
        transaction_type = self.request.query_params.get('type', None)
        account_id = self.request.query_params.get('account', None)
        category_id = self.request.query_params.get('category', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        search = self.request.query_params.get('search', None)
        
        if transaction_type:
            queryset = queryset.filter(type=transaction_type.upper())
        
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Resumo financeiro"""
        queryset = self.get_queryset()
        
        # Período (padrão: mês atual)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date:
            start_date = timezone.now().replace(day=1).date()
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        if not end_date:
            end_date = timezone.now().date()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        queryset = queryset.filter(date__range=[start_date, end_date])
        
        # Cálculos
        income = queryset.filter(type='INCOME').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense = queryset.filter(type='EXPENSE').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        balance = income - expense
        
        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'income': income,
            'expense': expense,
            'balance': balance,
            'transactions_count': queryset.count()
        })
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Transações agrupadas por categoria"""
        queryset = self.get_queryset()
        
        # Filtro por tipo (income ou expense)
        transaction_type = request.query_params.get('type', 'EXPENSE')
        
        queryset = queryset.filter(type=transaction_type.upper())
        
        # Agrupa por categoria
        categories = queryset.values(
            'category__id',
            'category__name',
            'category__icon'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Calcula percentual
        total = sum(cat['total'] for cat in categories)
        
        for cat in categories:
            cat['percentage'] = (cat['total'] / total * 100) if total > 0 else 0
        
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def monthly_evolution(self, request):
        """Evolução mensal de receitas e despesas"""
        # Últimos 6 meses
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=180)
        
        queryset = self.get_queryset().filter(
            date__range=[start_date, end_date]
        )
        
        # Agrupa por mês
        months = []
        current_date = start_date.replace(day=1)
        
        while current_date <= end_date:
            month_end = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            month_transactions = queryset.filter(
                date__range=[current_date, month_end]
            )
            
            income = month_transactions.filter(type='INCOME').aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            expense = month_transactions.filter(type='EXPENSE').aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            months.append({
                'month': current_date.strftime('%b'),
                'year': current_date.year,
                'income': float(income),
                'expense': float(expense),
                'balance': float(income - expense)
            })
            
            # Próximo mês
            current_date = (month_end + timedelta(days=1))
        
        return Response(months)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Dados completos para o dashboard"""
        user = request.user
        
        # Período: mês atual
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        
        # Transações do mês
        month_transactions = Transaction.objects.filter(
            user=user,
            date__range=[start_of_month, today]
        )
        
        # Totais
        income = month_transactions.filter(type='INCOME').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense = month_transactions.filter(type='EXPENSE').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Saldo total das contas
        from accounts.models import Account
        accounts = Account.objects.filter(user=user)
        total_balance = sum(acc.current_balance for acc in accounts)
        
        # Despesas por categoria
        expenses_by_category = month_transactions.filter(
            type='EXPENSE'
        ).values(
            'category__name',
            'category__icon'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')[:5]
        
        return Response({
            'total_balance': total_balance,
            'month_income': income,
            'month_expense': expense,
            'month_balance': income - expense,
            'top_expenses': list(expenses_by_category)
        })
