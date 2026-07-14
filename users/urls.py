from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import RegisterView, ProfileView

app_name = 'users'

urlpatterns = [
    # Регистрация
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT токены
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Профиль
    path('profile/', ProfileView.as_view(), name='profile'),
]