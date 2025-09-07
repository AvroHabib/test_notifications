from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from .models import User, UserDevice
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserDeviceSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    request=UserRegistrationSerializer,
    responses={201: UserProfileSerializer}
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return user profile data
        profile_serializer = UserProfileSerializer(user)
        return Response(profile_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=UserDeviceSerializer,
    responses={201: UserDeviceSerializer}
)
class RegisterDeviceView(generics.CreateAPIView):
    serializer_class = UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        device = serializer.save()
        return Response(UserDeviceSerializer(device).data, status=status.HTTP_201_CREATED)


@extend_schema(
    responses={200: UserProfileSerializer}
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@extend_schema(
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}}
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout user by deactivating all their devices
    """
    UserDevice.objects.filter(user=request.user).update(is_active=False)
    return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
