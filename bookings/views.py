from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Category, Resource, Booking, BookingStatus
from .serializers import (
    CategorySerializer, ResourceSerializer, 
    BookingListSerializer, BookingCreateSerializer, 
    BookingDetailSerializer, BookingUpdateStatusSerializer
)
from core.permissions import IsAdmin, IsTeacher, IsUser
from core.utils import check_resource_availability


# ------ Категории ------
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    Список и создание категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Детали, редактирование и удаление категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsAdmin()]


# ------ Ресурсы ------
class ResourceListCreateView(generics.ListCreateAPIView):
    """
    Список ресурсов и создание нового
    """
    queryset = Resource.objects.filter(is_active=True)
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтр по количеству (уникальные/множественные)
        is_unique = self.request.query_params.get('is_unique')
        if is_unique is not None:
            if is_unique.lower() == 'true':
                queryset = queryset.filter(total_quantity=1)
            elif is_unique.lower() == 'false':
                queryset = queryset.filter(total_quantity__gt=1)
        return queryset


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Детали, редактирование и удаление ресурса
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsAdmin()]


# ------ Бронирования ------
class BookingListCreateView(generics.ListCreateAPIView):
    """
    Список бронирований и создание нового
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'date', 'resource']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUser()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingListSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Админ видит все бронирования
        if user.is_staff:
            return Booking.objects.all().select_related('user', 'resource')
        
        # Обычные пользователи видят только свои
        return Booking.objects.filter(user=user).select_related('user', 'resource')


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Детали, редактирование и удаление бронирования
    """
    queryset = Booking.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        if self.request.method == 'DELETE':
            return [IsUser()]
        return [IsAdmin()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH'] and self.request.user.is_staff:
            return BookingUpdateStatusSerializer
        return BookingDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Booking.objects.all().select_related('user', 'resource')
        
        return Booking.objects.filter(user=user).select_related('user', 'resource')


class BookingCancelView(generics.GenericAPIView):
    """
    Отмена бронирования пользователем
    """
    permission_classes = [IsUser]
    serializer_class = BookingDetailSerializer
    
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        
        if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            return Response(
                {'error': f'Нельзя отменить бронирование со статусом "{booking.status}"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = BookingStatus.CANCELLED
        booking.save()
        
        return Response({
            'message': 'Бронирование отменено',
            'booking': BookingDetailSerializer(booking).data
        })


class BookingCheckAvailabilityView(generics.GenericAPIView):
    """
    Проверка доступности ресурса на определённое время
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        resource_id = request.query_params.get('resource_id')
        date = request.query_params.get('date')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        quantity = request.query_params.get('quantity', 1)
        
        if not all([resource_id, date, start_time, end_time]):
            return Response(
                {'error': 'Необходимо указать resource_id, date, start_time, end_time'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            is_available, message, available = check_resource_availability(
                resource_id, date, start_time, end_time, int(quantity)
            )
        except ValueError:
            return Response(
                {'error': 'Некорректный формат данных'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'is_available': is_available,
            'message': message,
            'available_count': available
        })