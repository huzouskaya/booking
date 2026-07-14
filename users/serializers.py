from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import UserProfile, UserRole

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя
    """
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'department', 'position', 'role')
        read_only_fields = ('id',)
    
    def get_role(self, obj):
        try:
            return obj.profile.role
        except:
            return UserRole.USER


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserRole.choices, required=False, default=UserRole.USER)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 
                  'first_name', 'last_name', 'phone', 'department', 'position', 'role')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        role = validated_data.pop('role', UserRole.USER)
        password = validated_data.pop('password')
        validated_data.pop('password2')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        # Создаём профиль
        UserProfile.objects.create(user=user, role=role)
        
        return user