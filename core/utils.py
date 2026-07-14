from datetime import datetime
from django.db.models import Q, Sum
from bookings.models import Booking, Resource, BookingStatus


def check_resource_availability(resource_id, date, start_time, end_time, quantity=1, exclude_booking_id=None):
    """
    Проверяет доступность ресурса на указанное время
    
    Returns:
        (is_available: bool, message: str, available_count: int)
    """
    try:
        resource = Resource.objects.get(id=resource_id, is_active=True)
    except Resource.DoesNotExist:
        return False, "Ресурс не найден", 0
    
    # Получаем все подтверждённые и ожидающие брони
    bookings = Booking.objects.filter(
        resource_id=resource_id,
        date=date,
        status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED],
    )
    
    if exclude_booking_id:
        bookings = bookings.exclude(id=exclude_booking_id)
    
    # Находим пересечения по времени
    overlapping = bookings.filter(
        Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
    )
    
    # Суммируем занятое количество
    used_quantity = overlapping.aggregate(total=Sum('quantity'))['total'] or 0
    
    available = resource.total_quantity - used_quantity
    
    if available < quantity:
        return False, f"Доступно только {available} из {quantity} запрошенных", available
    
    return True, "Доступно", available


def get_user_role(user):
    """
    Получить роль пользователя
    """
    if not user or not user.is_authenticated:
        return 'guest'
    
    if user.is_staff:
        return 'admin'
    
    try:
        return user.profile.role
    except:
        return 'user'