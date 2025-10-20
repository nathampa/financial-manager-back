# backend/accounts/serializers.py
from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    current_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Account
        fields = [
            'id', 'name', 'type', 'type_display', 'initial_balance',
            'current_balance', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'current_balance']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AccountListSerializer(serializers.ModelSerializer):
    """Serializer mais leve para listagens"""
    current_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'type', 'type_display', 'current_balance']