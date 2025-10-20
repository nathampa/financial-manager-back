# ==========================================
# backend/users/views.py
# ==========================================
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    ChangePasswordSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """Registro de novos usuários"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Perfil do usuário autenticado"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """Alteração de senha"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Verifica senha antiga
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Define nova senha
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"message": "Senha alterada com sucesso."},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """Estatísticas do usuário"""
    user = request.user
    
    stats = {
        'total_accounts': user.accounts.count(),
        'total_categories': user.categories.count(),
        'total_transactions': user.transactions.count(),
    }
    
    return Response(stats)

