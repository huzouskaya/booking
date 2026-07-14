import api from './api';
import type { Resource, Category, Booking, BookingCreate, AvailabilityResponse } from '../types';

// Категории
export const categoryService = {
    async getAll(): Promise<Category[]> {
        const response = await api.get('bookings/categories/');
        return response.data.results || response.data;
    },
};

// Ресурсы
export const resourceService = {
    async getAll(params?: { category?: number; search?: string; is_unique?: boolean }): Promise<Resource[]> {
        const response = await api.get<{ results: Resource[] }>('bookings/resources/', { params });
        return response.data.results;
    },

    async getById(id: number): Promise<Resource> {
        const response = await api.get<Resource>(`bookings/resources/${id}/`);
        return response.data;
    },

    async delete(id: number): Promise<void> {
        await api.delete(`bookings/resources/${id}/`);
    },

    async checkAvailability(
        resourceId: number,
        date: string,
        startTime: string,
        endTime: string,
        quantity: number = 1
    ): Promise<AvailabilityResponse> {
        const response = await api.get<AvailabilityResponse>('bookings/check-availability/', {
        params: {
            resource_id: resourceId,
            date,
            start_time: startTime,
            end_time: endTime,
            quantity,
        },
        });
        return response.data;
    },
};

// Бронирования
export const bookingService = {
    async getAll(params?: any): Promise<Booking[]> {
        const response = await api.get('bookings/', { params });
        console.log('📥 bookingService.getAll ответ:', response.data);
        return response.data.results || response.data;
    },

    async getById(id: number): Promise<Booking> {
        const response = await api.get<Booking>(`bookings/${id}/`);
        return response.data;
    },

    async create(data: BookingCreate): Promise<Booking> {
        const response = await api.post<Booking>('bookings/', data);
        return response.data;
    },

    async cancel(id: number): Promise<{ message: string }> {
        const response = await api.post<{ message: string }>(`bookings/${id}/cancel/`);
        return response.data;
    },

    async updateStatus(id: number, status: string, adminComment?: string): Promise<Booking> {
        const response = await api.patch<Booking>(`bookings/${id}/`, { status, admin_comment: adminComment });
        return response.data;
    },
};