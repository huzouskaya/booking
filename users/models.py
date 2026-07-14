from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя
    """
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    department = models.CharField(max_length=100, blank=True, verbose_name='Отдел')
    position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}".strip() or self.username


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    TEACHER = 'teacher', 'Преподаватель'
    USER = 'user', 'Пользователь'
    GUEST = 'guest', 'Гость'


class UserProfile(models.Model):
    """
    Профиль пользователя с ролью
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='Пользователь'
    )
    role = models.CharField(
        max_length=20, 
        choices=UserRole.choices, 
        default=UserRole.USER,
        verbose_name='Роль'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name='Аватар'
    )
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"