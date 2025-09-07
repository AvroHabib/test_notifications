from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    UserRegistrationView,
    RegisterDeviceView,
    UserProfileView,
    logout_view
)

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('logout/', logout_view, name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Device registration
    path('device/register/', RegisterDeviceView.as_view(), name='device-register'),
]
