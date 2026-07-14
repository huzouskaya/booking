from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешение только для администраторов
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsTeacher(permissions.BasePermission):
    """
    Разрешение для преподавателей и выше
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            return request.user.profile.role in ['admin', 'teacher']
        except:
            return False


class IsUser(permissions.BasePermission):
    """
    Разрешение для авторизованных пользователей (не гостей)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated