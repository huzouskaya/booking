<template>
  <div class="resources-page">
    <h1>📚 Каталог ресурсов</h1>

    <!-- Фильтры с защитой от null -->
    <div class="filters">
      <div class="filter-group">
        <label for="category">Категория:</label>
        <select id="category" v-model="filters.category" @change="applyFilters">
          <option value="">Все категории</option>
          <option 
            v-for="category in categories" 
            :key="category?.id || `cat-${Math.random()}`" 
            :value="category?.id || ''"
          >
            {{ category?.name || 'Без названия' }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label for="search">Поиск:</label>
        <input
          id="search"
          v-model="filters.search"
          type="text"
          placeholder="Название ресурса..."
          @input="applyFilters"
        />
      </div>

      <button @click="resetFilters" class="btn-secondary">Сбросить</button>
    </div>

    <!-- Список ресурсов -->
    <div v-if="loading" class="loading">Загрузка...</div>
    
    <div v-else-if="resources.length === 0" class="empty">
      <p>Ресурсы не найдены</p>
    </div>

    <div v-else class="resources-grid">
      <div
        v-for="resource in resources"
        :key="resource.id"
        class="resource-card"
        @click="goToResource(resource.id)"
      >
        <div class="resource-image">
          <span v-if="!resource.image" class="placeholder">📦</span>
          <img v-else :src="resource.image" :alt="resource.name" />
        </div>
        
        <div class="resource-info">
          <h3>{{ resource.name }}</h3>
          <p class="category">{{ resource.category?.name || 'Без категории' }}</p>
          <p class="description">{{ resource.description?.slice(0, 100) || '' }}</p>
          <div class="meta">
            <span>📍 {{ resource.location || 'Место не указано' }}</span>
            <span>{{ resource.total_quantity }} шт.</span>
            <span v-if="resource.is_unique">⭐ Уникальный</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { resourceService, categoryService } from '../services/resourcesService';
import type { Resource, Category } from '../types';

const router = useRouter();
const resources = ref<Resource[]>([]);
const categories = ref<Category[]>([]);
const loading = ref(false);

const filters = ref({
  category: '',
  search: '',
});

const loadResources = async () => {
  loading.value = true;
  try {
    const params: any = {};
    if (filters.value.category) params.category = filters.value.category;
    if (filters.value.search) params.search = filters.value.search;
    
    const data = await resourceService.getAll(params);
    resources.value = data;
  } catch (error) {
    console.error('❌ Ошибка загрузки ресурсов:', error);
  } finally {
    loading.value = false;
  }
};

const loadCategories = async () => {
  try {
    const data = await categoryService.getAll();
    categories.value = data;
  } catch (error) {
    console.error('❌ Ошибка загрузки категорий:', error);
  }
};

const applyFilters = () => {
  loadResources();
};

const resetFilters = () => {
  filters.value.category = '';
  filters.value.search = '';
  loadResources();
};

const goToResource = (id: number) => {
  router.push(`/resources/${id}`);
};

onMounted(() => {
  loadCategories();
  loadResources();
});
</script>

<style scoped>
.resources-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 30px;
  color: #2c3e50;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: end;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 30px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: 500;
  font-size: 14px;
  color: #2c3e50;
}

.filter-group input,
.filter-group select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 150px;
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-color: #3498db;
}

.btn-secondary {
  padding: 8px 20px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.resource-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.resource-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.resource-image {
  height: 150px;
  background: #ecf0f1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.resource-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.resource-info {
  padding: 15px;
}

.resource-info h3 {
  margin: 0 0 5px 0;
  color: #2c3e50;
}

.resource-info .category {
  color: #3498db;
  font-size: 14px;
  margin: 0 0 10px 0;
}

.resource-info .description {
  color: #7f8c8d;
  font-size: 14px;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #95a5a6;
  flex-wrap: wrap;
  gap: 5px;
}

.loading,
.empty {
  text-align: center;
  padding: 50px;
  color: #7f8c8d;
}
</style>