# backend/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegistrationView,
    UserProfileView,
    ChangePasswordView,
    user_stats
)

urlpatterns = [
    # Autenticação JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Usuários
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('stats/', user_stats, name='user-stats'),
]