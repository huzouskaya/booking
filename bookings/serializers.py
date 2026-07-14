from rest_framework import serializers
from django.db import transaction
from .models import Category, Resource, Booking, BookingStatus
from core.utils import check_resource_availability
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'icon', 'created_at')
        read_only_fields = ('id', 'created_at')


class ResourceSerializer(serializers.ModelSerializer):
    """
    Сериализатор ресурса
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True
    )
    
    class Meta:
        model = Resource
        fields = ('id', 'name', 'description', 'category', 'category_id', 
                    'total_quantity', 'image', 'is_active', 'location', 
                    'specifications', 'is_unique', 'created_at')
        read_only_fields = ('id', 'created_at', 'is_unique')

class BookingListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'resource', 'date',
                    'start_time', 'end_time', 'quantity', 'status', 'comment', 'created_at')

class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания бронирования
    """
    class Meta:
        model = Booking
        fields = ('resource', 'date', 'start_time', 'end_time', 'quantity', 'comment')
    
    def validate(self, attrs):
        """
        Проверка доступности ресурса
        """
        resource = attrs['resource']
        date = attrs['date']
        start_time = attrs['start_time']
        end_time = attrs['end_time']
        quantity = attrs.get('quantity', 1)
        
        if start_time >= end_time:
            raise serializers.ValidationError("Время начала должно быть раньше времени окончания")
        
        is_available, message, available = check_resource_availability(
            resource.id, date, start_time, end_time, quantity
        )
        
        if not is_available:
            raise serializers.ValidationError(message)
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = BookingStatus.PENDING
        return super().create(validated_data)


class BookingDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального просмотра бронирования
    """
    user = UserSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'resource', 'date', 'start_time', 'end_time', 
                    'quantity', 'status', 'comment', 'admin_comment', 'created_at', 'updated_at')


class BookingUpdateStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления статуса бронирования (админ)
    """
    class Meta:
        model = Booking
        fields = ('status', 'admin_comment')
    
    def validate_status(self, value):
        valid_statuses = [BookingStatus.CONFIRMED, BookingStatus.REJECTED, BookingStatus.COMPLETED]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Недопустимый статус. Доступны: {valid_statuses}")
        return value