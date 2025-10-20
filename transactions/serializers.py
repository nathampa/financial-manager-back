# backend/transactions/serializers.py
from rest_framework import serializers
from .models import Transaction
from accounts.serializers import AccountListSerializer
from categories.serializers import CategorySerializer

class TransactionSerializer(serializers.ModelSerializer):
    account_detail = AccountListSerializer(source='account', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'description', 'amount', 'type', 'type_display',
            'date', 'account', 'category', 'account_detail',
            'category_detail', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        
        # Valida se a conta pertence ao usuário
        if attrs['account'].user != user:
            raise serializers.ValidationError(
                {"account": "Esta conta não pertence ao usuário."}
            )
        
        # Valida se a categoria pertence ao usuário ou é do sistema
        category = attrs['category']
        if category.user and category.user != user:
            raise serializers.ValidationError(
                {"category": "Esta categoria não pertence ao usuário."}
            )
        
        return attrs


class TransactionListSerializer(serializers.ModelSerializer):
    """Serializer mais leve para listagens"""
    account_name = serializers.CharField(source='account.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'description', 'amount', 'type', 'type_display',
            'date', 'account_name', 'category_name', 'category_icon'
        ]