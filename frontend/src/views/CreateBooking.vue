<template>
  <div class="booking-form">
    <h1>📅 Создание бронирования</h1>
    
    <div v-if="resource" class="form-card">
      <div class="resource-info">
        <h3>{{ resource.name }}</h3>
        <p>{{ resource.category.name }} • {{ resource.location || 'Место не указано' }}</p>
        <p>Доступно: {{ resource.total_quantity }} шт.</p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="date">Дата *</label>
          <input
            id="date"
            v-model="form.date"
            type="date"
            :min="minDate"
            required
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="start_time">Время начала *</label>
            <input
              id="start_time"
              v-model="form.start_time"
              type="time"
              required
              @change="checkAvailability"
            />
          </div>

          <div class="form-group">
            <label for="end_time">Время окончания *</label>
            <input
              id="end_time"
              v-model="form.end_time"
              type="time"
              required
              @change="checkAvailability"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="quantity">Количество</label>
          <input
            id="quantity"
            v-model.number="form.quantity"
            type="number"
            min="1"
            :max="resource.total_quantity"
          />
        </div>

        <div class="form-group">
          <label for="comment">Комментарий</label>
          <textarea
            id="comment"
            v-model="form.comment"
            rows="3"
            placeholder="Дополнительная информация..."
          />
        </div>

        <!-- Статус доступности -->
        <div v-if="availabilityChecked" class="availability-status">
          <div v-if="isAvailable" class="available">
            ✅ {{ availabilityMessage }}
          </div>
          <div v-else class="unavailable">
            ❌ {{ availabilityMessage }}
          </div>
        </div>

        <button
          type="submit"
          :disabled="!isAvailable || loading"
          class="btn-submit"
        >
          {{ loading ? 'Создание...' : 'Забронировать' }}
        </button>
      </form>
    </div>

    <div v-else class="loading">Загрузка...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { resourceService, bookingService } from '../services/resourcesService';
import { useAuthStore } from '../stores/authStore';
import type { Resource } from '../types';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const resource = ref<Resource | null>(null);
const loading = ref(false);
const availabilityChecked = ref(false);
const isAvailable = ref(false);
const availabilityMessage = ref('');

const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

const form = reactive({
  resource: Number(route.query.resource) || 0,
  date: '',
  start_time: '',
  end_time: '',
  quantity: 1,
  comment: '',
});

const loadResource = async () => {
  if (!form.resource) {
    router.push('/resources');
    return;
  }
  
  try {
    resource.value = await resourceService.getById(form.resource);
    if (!resource.value.is_active) {
      alert('Этот ресурс недоступен');
      router.push('/resources');
    }
  } catch (error) {
    console.error('Ошибка загрузки ресурса:', error);
    router.push('/resources');
  }
};

const checkAvailability = async () => {
  if (!form.date || !form.start_time || !form.end_time) return;
  
  if (form.start_time >= form.end_time) {
    availabilityChecked.value = true;
    isAvailable.value = false;
    availabilityMessage.value = 'Время начала должно быть раньше времени окончания';
    return;
  }

  try {
    const result = await resourceService.checkAvailability(
      form.resource,
      form.date,
      form.start_time,
      form.end_time,
      form.quantity
    );
    
    availabilityChecked.value = true;
    isAvailable.value = result.is_available;
    availabilityMessage.value = result.message;
  } catch (error) {
    console.error('Ошибка проверки доступности:', error);
  }
};

const handleSubmit = async () => {
  if (!isAvailable.value) {
    alert('Ресурс недоступен в выбранное время');
    return;
  }

  loading.value = true;
  try {
    const booking = await bookingService.create(form);
    alert('Бронирование создано!');
    router.push('/bookings');
  } catch (error: any) {
    console.error('Ошибка создания бронирования:', error);
    alert(error.response?.data?.detail || 'Ошибка создания бронирования');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadResource();
});
</script>

<style scoped>
.booking-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.form-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.resource-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 25px;
}

.resource-info h3 {
  margin: 0 0 5px 0;
  color: #2c3e50;
}

.resource-info p {
  margin: 3px 0;
  color: #7f8c8d;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.availability-status {
  padding: 15px;
  border-radius: 8px;
  margin: 20px 0;
}

.available {
  background: #d5f5e3;
  color: #27ae60;
  padding: 10px;
  border-radius: 6px;
}

.unavailable {
  background: #fadbd8;
  color: #e74c3c;
  padding: 10px;
  border-radius: 6px;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: #2980b9;
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #7f8c8d;
}
</style>