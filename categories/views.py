# backend/categories/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD completo de categorias"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna categorias do usuário + categorias do sistema"""
        user = self.request.user
        return Category.objects.filter(
            Q(user=user) | Q(user__isnull=True)
        )
    
    def destroy(self, request, *args, **kwargs):
        """Impede exclusão de categorias do sistema"""
        instance = self.get_object()
        
        if instance.user is None:
            return Response(
                {"error": "Categorias do sistema não podem ser excluídas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if instance.transactions.exists():
            return Response(
                {"error": "Não é possível excluir categoria com transações associadas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Lista categorias separadas por tipo"""
        queryset = self.get_queryset()
        
        income_categories = CategorySerializer(
            queryset.filter(type='INCOME'),
            many=True
        ).data
        
        expense_categories = CategorySerializer(
            queryset.filter(type='EXPENSE'),
            many=True
        ).data
        
        return Response({
            'income': income_categories,
            'expense': expense_categories
        })
