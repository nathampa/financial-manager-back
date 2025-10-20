# ==========================================
# backend/accounts/views.py
# ==========================================
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .serializers import AccountSerializer, AccountListSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """CRUD completo de contas"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AccountListSerializer
        return AccountSerializer
    
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Resumo de todas as contas"""
        accounts = self.get_queryset()
        
        total_balance = sum(acc.current_balance for acc in accounts)
        
        summary = {
            'total_accounts': accounts.count(),
            'total_balance': total_balance,
            'accounts_by_type': {}
        }
        
        for account in accounts:
            acc_type = account.get_type_display()
            if acc_type not in summary['accounts_by_type']:
                summary['accounts_by_type'][acc_type] = {
                    'count': 0,
                    'balance': 0
                }
            summary['accounts_by_type'][acc_type]['count'] += 1
            summary['accounts_by_type'][acc_type]['balance'] += float(account.current_balance)
        
        return Response(summary)