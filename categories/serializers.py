# backend/categories/serializers.py
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    is_system = serializers.SerializerMethodField()
    transactions_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'type', 'type_display', 'icon',
            'is_system', 'transactions_count'
        ]
        read_only_fields = ['id', 'is_system']

    def get_is_system(self, obj):
        return obj.user is None

    def get_transactions_count(self, obj):
        return obj.transactions.count()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, attrs):
        # Impede edição de categorias do sistema
        if self.instance and self.instance.user is None:
            raise serializers.ValidationError(
                "Categorias do sistema não podem ser editadas."
            )
        return attrs