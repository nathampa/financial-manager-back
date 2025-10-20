# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import AccountViewSet
from categories.views import CategoryViewSet
from transactions.views import TransactionViewSet

# Router para viewsets
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include([
        # Auth e Users
        path('auth/', include('users.urls')),
        
        # Router endpoints
        path('', include(router.urls)),
    ])),
]