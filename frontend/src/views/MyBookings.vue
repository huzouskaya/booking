<template>
  <div class="my-bookings">
    <h1>📋 Мои бронирования</h1>

    <div class="filters">
      <select v-model="statusFilter" @change="loadBookings">
        <option value="">Все статусы</option>
        <option value="pending">Ожидает</option>
        <option value="confirmed">Подтверждено</option>
        <option value="rejected">Отклонено</option>
        <option value="completed">Завершено</option>
        <option value="cancelled">Отменено</option>
      </select>
    </div>
    
    <div v-if="bookings.length === 0" class="empty">
      <p>У вас пока нет бронирований</p>
      <router-link to="/resources" class="btn-primary">Перейти к каталогу</router-link>
    </div>

    <div v-else class="bookings-list">
      <div
        v-for="booking in bookings"
        :key="booking.id"
        class="booking-card"
        :class="booking.status"
      >
        <div class="booking-header">
          <h3>{{ booking.resource.name }}</h3>
          <span class="status-badge">{{ getStatusLabel(booking.status) }}</span>
        </div>

        <div class="booking-body">
          <p><strong>Дата:</strong> {{ formatDate(booking.date) }}</p>
          <p><strong>Время:</strong> {{ booking.start_time }} - {{ booking.end_time }}</p>
          <p><strong>Количество:</strong> {{ booking.quantity }} шт.</p>
          <p v-if="booking.comment"><strong>Комментарий:</strong> {{ booking.comment }}</p>
          <p v-if="booking.admin_comment" class="admin-comment">
            <strong>Комментарий администратора:</strong> {{ booking.admin_comment }}
          </p>
        </div>

        <div class="booking-actions">
          <button
            v-if="canCancel(booking.status)"
            @click="cancelBooking(booking.id)"
            class="btn-cancel"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { bookingService } from '../services/resourcesService';
import type { Booking } from '../types';

const bookings = ref<Booking[]>([]);
const loading = ref(false);
const statusFilter = ref('');

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    pending: '⏳ Ожидает',
    confirmed: '✅ Подтверждено',
    rejected: '❌ Отклонено',
    completed: '✔️ Завершено',
    cancelled: '⛔ Отменено',
  };
  return labels[status] || status;
};

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('ru-RU');
};

const canCancel = (status: string) => {
  return status === 'pending' || status === 'confirmed';
};

const loadBookings = async () => {
  loading.value = true;
  try {
    const params: any = {};
    if (statusFilter.value) params.status = statusFilter.value;
    const data = await bookingService.getAll(params);
    console.log('📥 Получены бронирования:', data);
    bookings.value = data;
  } catch (error) {
    console.error('Ошибка загрузки бронирований:', error);
    bookings.value = [];
  }
};

const cancelBooking = async (id: number) => {
  if (!confirm('Вы уверены, что хотите отменить бронирование?')) return;
  
  try {
    await bookingService.cancel(id);
    alert('Бронирование отменено');
    await loadBookings();
  } catch (error) {
    console.error('Ошибка отмены:', error);
    alert('Не удалось отменить бронирование');
  }
};

onMounted(() => {
  loadBookings();
});
</script>

<style scoped>
.my-bookings {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.filters {
  margin-bottom: 30px;
}

.filters select {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.booking-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-left: 4px solid #95a5a6;
}

.booking-card.pending {
  border-left-color: #f39c12;
}

.booking-card.confirmed {
  border-left-color: #2ecc71;
}

.booking-card.rejected {
  border-left-color: #e74c3c;
}

.booking-card.completed {
  border-left-color: #3498db;
}

.booking-card.cancelled {
  border-left-color: #95a5a6;
  opacity: 0.7;
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.booking-header h3 {
  margin: 0;
  color: #2c3e50;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.booking-card.pending .status-badge {
  background: #fef9e7;
  color: #f39c12;
}

.booking-card.confirmed .status-badge {
  background: #d5f5e3;
  color: #27ae60;
}

.booking-card.rejected .status-badge {
  background: #fadbd8;
  color: #e74c3c;
}

.booking-card.completed .status-badge {
  background: #d6eaf8;
  color: #2980b9;
}

.booking-card.cancelled .status-badge {
  background: #ecf0f1;
  color: #7f8c8d;
}

.booking-body p {
  margin: 5px 0;
  color: #2c3e50;
}

.admin-comment {
  margin-top: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  color: #7f8c8d;
}

.booking-actions {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ecf0f1;
}

.btn-cancel {
  padding: 8px 20px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-cancel:hover {
  background: #c0392b;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #7f8c8d;
}

.empty {
  text-align: center;
  padding: 50px;
  color: #7f8c8d;
}

.empty .btn-primary {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 30px;
  background: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 6px;
}

.empty .btn-primary:hover {
  background: #2980b9;
}
</style>