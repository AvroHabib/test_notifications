from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User, UserDevice


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        
        if phone_number and password:
            user = authenticate(username=phone_number, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid phone number or password.')
        else:
            raise serializers.ValidationError('Must include phone number and password.')


class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ('fcm_token', 'device_type', 'device_id')
    
    def create(self, validated_data):
        user = self.context['request'].user
        # Deactivate old tokens for the same device
        UserDevice.objects.filter(
            user=user,
            device_id=validated_data.get('device_id', '')
        ).update(is_active=False)
        
        device, created = UserDevice.objects.update_or_create(
            user=user,
            fcm_token=validated_data['fcm_token'],
            defaults=validated_data
        )
        return device


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'profile_picture', 'date_joined')
        read_only_fields = ('id', 'phone_number', 'date_joined')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the username field since we're using phone_number
        if 'username' in self.fields:
            del self.fields['username']
    
    def validate(self, attrs):
        # Use phone_number as username for authentication
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        
        if not phone_number or not password:
            raise serializers.ValidationError('Must include phone number and password.')
        
        # Authenticate using phone_number as username
        from django.contrib.auth import authenticate
        user = authenticate(username=phone_number, password=password)
        
        if user is None:
            raise serializers.ValidationError('Invalid phone number or password.')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        
        # Get tokens
        refresh = self.get_token(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['phone_number'] = user.phone_number
        token['full_name'] = user.get_full_name()
        return token
