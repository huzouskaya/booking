from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Категория ресурса
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Иконка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    Ресурс для бронирования (аудитория, оборудование и т.д.)
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='resources',
        verbose_name='Категория'
    )
    total_quantity = models.PositiveIntegerField(
        default=1, 
        help_text='1 — уникальный объект (аудитория), >1 — несколько экземпляров',
        verbose_name='Общее количество'
    )
    image = models.ImageField(
        upload_to='resources/', 
        blank=True, 
        null=True,
        verbose_name='Изображение'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    location = models.CharField(max_length=200, blank=True, verbose_name='Расположение')
    specifications = models.JSONField(default=dict, blank=True, verbose_name='Характеристики')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'resources'
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (x{self.total_quantity})"
    
    @property
    def is_unique(self):
        return self.total_quantity == 1


class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Ожидает подтверждения'
    CONFIRMED = 'confirmed', 'Подтверждено'
    REJECTED = 'rejected', 'Отклонено'
    COMPLETED = 'completed', 'Завершено'
    CANCELLED = 'cancelled', 'Отменено пользователем'


class Booking(models.Model):
    """
    Бронирование ресурса
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name='Пользователь'
    )
    resource = models.ForeignKey(
        Resource, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name='Ресурс'
    )
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    quantity = models.PositiveIntegerField(
        default=1, 
        help_text='Количество экземпляров',
        verbose_name='Количество'
    )
    status = models.CharField(
        max_length=20, 
        choices=BookingStatus.choices, 
        default=BookingStatus.PENDING,
        verbose_name='Статус'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    admin_comment = models.TextField(blank=True, verbose_name='Комментарий администратора')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['resource', 'date', 'start_time', 'end_time']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.resource.name} - {self.date}"
    
    def is_overlapping(self, other_booking):
        """
        Проверка пересечения с другим бронированием
        """
        if self.resource_id != other_booking.resource_id:
            return False
        if self.date != other_booking.date:
            return False
        return (self.start_time < other_booking.end_time and 
                self.end_time > other_booking.start_time)