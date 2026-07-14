from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ResourceListCreateView, ResourceDetailView,
    BookingListCreateView, BookingDetailView,
    BookingCancelView, BookingCheckAvailabilityView,
)

app_name = 'bookings'

urlpatterns = [
    # Категории
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Ресурсы
    path('resources/', ResourceListCreateView.as_view(), name='resource-list'),
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    
    # Проверка доступности
    path('check-availability/', BookingCheckAvailabilityView.as_view(), name='check-availability'),
    
    # Бронирования
    path('', BookingListCreateView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]