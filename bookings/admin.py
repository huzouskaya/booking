# bookings/admin.py
from django.contrib import admin
from .models import Category, Resource, Booking


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'total_quantity', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('total_quantity', 'is_active')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'date', 'resource__category')
    search_fields = ('user__username', 'resource__name')
    readonly_fields = ('created_at', 'updated_at')