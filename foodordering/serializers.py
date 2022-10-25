from rest_framework import serializers
from .models import User, Store, Item
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email', 'name', 'user_type', 'is_active', ]

class RegisterUserSerializer(serializers.ModelSerializer):
    PASSWORD_HELP_TEXT = "Please include the numbers and symbols for the strong password."
    
    password = serializers.CharField(required=True, write_only=True, min_length=8, max_length=60, help_text=PASSWORD_HELP_TEXT)
    retype_password = serializers.CharField(required=True,write_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'password', 'retype_password', 'email', 'user_type', 'is_active', ]
    
    '''
    Validating the password
    '''
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('retype_password'):
            raise serializers.ValidationError("Passwords must be same")
        
        return attrs 

    '''
    Creating the user
    '''
    def create(self, validated_data):
        validated_data.pop('retype_password', None)
        new_user = User.objects.create_user(**validated_data)
        return new_user

class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'access','refresh',]

    '''
    Validating the user credentials
    '''
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username
            }
            return validation

        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('pk', 'name', 'store_address', 'latitude', 'longitude', 'is_active', 'merchant')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('pk', 'name', 'price', 'description', 'is_active', 'stores')


    
