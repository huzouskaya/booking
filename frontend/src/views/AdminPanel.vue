<template>
  <div class="admin-panel">
    <h1>⚙️ Административная панель</h1>

    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Ресурсы -->
    <div v-if="activeTab === 'resources'" class="tab-content">
      <div class="toolbar">
        <h2>Управление ресурсами</h2>
        <button @click="openCreateResource" class="btn-primary">+ Добавить ресурс</button>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Категория</th>
              <th>Количество</th>
              <th>Статус</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="resource in resources" :key="resource.id">
              <td>{{ resource.id }}</td>
              <td>{{ resource.name }}</td>
              <td>{{ resource.category.name }}</td>
              <td>{{ resource.total_quantity }}</td>
              <td>
                <span :class="['status-badge', resource.is_active ? 'active' : 'inactive']">
                  {{ resource.is_active ? 'Активен' : 'Неактивен' }}
                </span>
              </td>
              <td>
                <button @click="editResource(resource)" class="btn-edit">✏️</button>
                <button @click="deleteResource(resource.id)" class="btn-delete">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Бронирования -->
    <div v-if="activeTab === 'bookings'" class="tab-content">
      <div class="toolbar">
        <h2>Управление бронированиями</h2>
        <div class="filters">
          <select v-model="adminBookingFilter" @change="loadAllBookings">
            <option value="">Все статусы</option>
            <option value="pending">Ожидает</option>
            <option value="confirmed">Подтверждено</option>
            <option value="rejected">Отклонено</option>
            <option value="completed">Завершено</option>
            <option value="cancelled">Отменено</option>
          </select>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Пользователь</th>
              <th>Ресурс</th>
              <th>Дата/Время</th>
              <th>Статус</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in allBookings" :key="booking.id">
              <td>{{ booking.id }}</td>
              <td>{{ booking.user.username }}</td>
              <td>{{ booking.resource.name }}</td>
              <td>{{ booking.date }} {{ booking.start_time }}-{{ booking.end_time }}</td>
              <td>
                <span :class="['status-badge', booking.status]">
                  {{ getStatusLabel(booking.status) }}
                </span>
              </td>
              <td>
                <select
                  v-model="booking.status"
                  @change="updateBookingStatus(booking.id, booking.status)"
                  class="status-select"
                >
                  <option value="pending">Ожидает</option>
                  <option value="confirmed">Подтвердить</option>
                  <option value="rejected">Отклонить</option>
                  <option value="completed">Завершить</option>
                  <option value="cancelled">Отменить</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { resourceService, bookingService } from '../services/resourcesService';
import type { Resource, Booking } from '../types';

const tabs = [
  { key: 'resources', label: '📦 Ресурсы' },
  { key: 'bookings', label: '📋 Бронирования' },
];

const activeTab = ref('resources');
const resources = ref<Resource[]>([]);
const allBookings = ref<Booking[]>([]);
const adminBookingFilter = ref('');

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

const loadResources = async () => {
  try {
    resources.value = await resourceService.getAll({ is_active: undefined });
  } catch (error) {
    console.error('Ошибка загрузки ресурсов:', error);
  }
};

const loadAllBookings = async () => {
  try {
    const params: any = {};
    if (adminBookingFilter.value) params.status = adminBookingFilter.value;
    allBookings.value = await bookingService.getAll(params);
  } catch (error) {
    console.error('Ошибка загрузки бронирований:', error);
  }
};

const updateBookingStatus = async (id: number, status: string) => {
  try {
    await bookingService.updateStatus(id, status);
    alert('Статус обновлён');
  } catch (error) {
    console.error('Ошибка обновления статуса:', error);
    alert('Не удалось обновить статус');
    loadAllBookings();
  }
};

const deleteResource = async (id: number) => {
  if (!confirm('Удалить ресурс?')) return;
  try {
    // API для удаления ресурса
    await resourceService.delete(id);
    alert('Ресурс удалён');
    loadResources();
  } catch (error) {
    console.error('Ошибка удаления:', error);
    alert('Не удалось удалить ресурс');
  }
};

const openCreateResource = () => {
  alert('Форма создания ресурса (в разработке)');
};

const editResource = (resource: Resource) => {
  alert(`Редактирование ресурса: ${resource.name} (в разработке)`);
};

onMounted(() => {
  loadResources();
  loadAllBookings();
});
</script>

<style scoped>
.admin-panel {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 2px solid #ecf0f1;
}

.tab-btn {
  padding: 12px 24px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 16px;
  color: #7f8c8d;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #2c3e50;
}

.tab-btn.active {
  color: #3498db;
  border-bottom-color: #3498db;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.toolbar h2 {
  margin: 0;
  color: #2c3e50;
}

.filters select {
  padding: 8px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.btn-primary {
  padding: 8px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-primary:hover {
  background: #2980b9;
}

.table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8f9fa;
}

th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
}

td {
  padding: 12px 15px;
  border-top: 1px solid #ecf0f1;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
}

.status-badge.active {
  background: #d5f5e3;
  color: #27ae60;
}

.status-badge.inactive {
  background: #fadbd8;
  color: #e74c3c;
}

.status-badge.pending {
  background: #fef9e7;
  color: #f39c12;
}

.status-badge.confirmed {
  background: #d5f5e3;
  color: #27ae60;
}

.status-badge.rejected {
  background: #fadbd8;
  color: #e74c3c;
}

.status-badge.completed {
  background: #d6eaf8;
  color: #2980b9;
}

.status-badge.cancelled {
  background: #ecf0f1;
  color: #7f8c8d;
}

.btn-edit,
.btn-delete {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-edit {
  background: #d6eaf8;
  color: #2980b9;
  margin-right: 5px;
}

.btn-edit:hover {
  background: #aed6f1;
}

.btn-delete {
  background: #fadbd8;
  color: #e74c3c;
}

.btn-delete:hover {
  background: #f5b7b1;
}

.status-select {
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>