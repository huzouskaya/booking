<template>
  <div v-if="resource" class="resource-detail">
    <button @click="$router.back()" class="btn-back">← Назад</button>

    <div class="detail-card">
      <div class="detail-header">
        <h1>{{ resource.name }}</h1>
        <span class="category-badge">{{ resource.category.name }}</span>
      </div>

      <div class="detail-body">
        <div class="detail-image">
          <span v-if="!resource.image" class="placeholder">📦</span>
          <img v-else :src="resource.image" :alt="resource.name" />
        </div>

        <div class="detail-info">
          <p class="description">{{ resource.description }}</p>
          
          <div class="specs">
            <div class="spec-item">
              <strong>📍 Местоположение:</strong>
              <span>{{ resource.location || 'Не указано' }}</span>
            </div>
            <div class="spec-item">
              <strong>📦 Количество:</strong>
              <span>{{ resource.total_quantity }} шт.</span>
            </div>
            <div class="spec-item">
              <strong>⭐ Тип:</strong>
              <span>{{ resource.is_unique ? 'Уникальный' : 'Множественный' }}</span>
            </div>
            <div v-if="resource.specifications && Object.keys(resource.specifications).length" class="spec-item">
              <strong>🔧 Характеристики:</strong>
              <ul>
                <li v-for="(value, key) in resource.specifications" :key="key">
                  {{ key }}: {{ value }}
                </li>
              </ul>
            </div>
          </div>

          <button v-if="authStore.isAuthenticated" @click="goToBooking" class="btn-book">
            📅 Забронировать
          </button>
          <p v-else class="auth-warning">Войдите, чтобы забронировать</p>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading">Загрузка...</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { resourceService } from '../services/resourcesService';
import { useAuthStore } from '../stores/authStore';
import type { Resource } from '../types';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const resource = ref<Resource | null>(null);

const loadResource = async () => {
  const id = Number(route.params.id);
  if (!id) return;
  
  try {
    resource.value = await resourceService.getById(id);
  } catch (error) {
    console.error('Ошибка загрузки ресурса:', error);
  }
};

const goToBooking = () => {
  router.push(`/bookings/create?resource=${resource.value?.id}`);
};

onMounted(() => {
  loadResource();
});
</script>

<style scoped>
.resource-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.btn-back {
  background: none;
  border: none;
  color: #3498db;
  font-size: 16px;
  cursor: pointer;
  padding: 10px 0;
  margin-bottom: 20px;
}

.btn-back:hover {
  color: #2980b9;
}

.detail-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  overflow: hidden;
}

.detail-header {
  padding: 30px 30px 20px;
  border-bottom: 1px solid #ecf0f1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.detail-header h1 {
  margin: 0;
  color: #2c3e50;
}

.category-badge {
  background: #3498db;
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
}

.detail-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  padding: 30px;
}

.detail-image {
  height: 300px;
  background: #ecf0f1;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5rem;
}

.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.description {
  font-size: 16px;
  line-height: 1.6;
  color: #2c3e50;
  margin: 0;
}

.specs {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.spec-item {
  margin: 8px 0;
}

.spec-item ul {
  margin: 5px 0 0 20px;
  padding: 0;
}

.spec-item li {
  margin: 3px 0;
}

.btn-book {
  padding: 12px 30px;
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
  align-self: start;
}

.btn-book:hover {
  background: #27ae60;
}

.auth-warning {
  color: #e74c3c;
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .detail-body {
    grid-template-columns: 1fr;
  }
}
</style>