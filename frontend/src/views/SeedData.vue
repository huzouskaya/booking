<template>
    <div class="seed-page">
        <div class="card">
            <h1>📦 Заполнение базы данных</h1>
            <p>Нажмите кнопку, чтобы создать тестовые категории и ресурсы</p>

            <div class="actions">
                <button @click="seedDatabase" :disabled="loading" class="btn-success">
                {{ loading ? 'Создание...' : '➕ Создать тестовые данные' }}
                </button>
            </div>

            <div v-if="result" class="result" :class="{ success: result.success, error: !result.success }">
                {{ result.message }}
                <p v-if="result.error" class="error-detail">{{ result.error }}</p>
            </div>
        </div>

        <div class="card">
            <h2>📋 Что будет создано</h2>
            <ul>
                <li>5 категорий (Аудитории, Компьютерные классы, Лаборатории, Переговорные, Оборудование)</li>
                <li>6 ресурсов с разными характеристиками</li>
                <li>Уникальные и множественные ресурсы</li>
            </ul>
        </div>

        <router-link to="/resources" class="btn-primary">Перейти к каталогу</router-link>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { seedService } from '../services/seedService';

const loading = ref(false);
const result = ref<{ success: boolean; message: string; error?: any } | null>(null);

const seedDatabase = async () => {
    loading.value = true;
    result.value = null;

    try {
        const response = await seedService.seedDatabase();
        console.log('Ответ от сервера:', response);
        
        if (response && typeof response === 'object') {
            result.value = {
                success: response.success ?? false,
                message: response.message || 'Операция выполнена',
                error: response.error || null
            };
        } else {
            result.value = {
                success: false,
                message: 'Неизвестный ответ от сервера',
                error: null
            };
        }
    } catch (error) {
        console.error('Ошибка:', error);
        result.value = {
            success: false,
            message: 'Ошибка при выполнении запроса',
            error: error
        };
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.seed-page {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
}

.card {
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}

h1, h2 {
    color: #2c3e50;
}

.actions {
    margin: 20px 0;
}

.btn-success {
    padding: 12px 30px;
    background: #2ecc71;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
}

.btn-success:hover:not(:disabled) {
    background: #27ae60;
}

.btn-success:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.result {
    padding: 15px;
    border-radius: 6px;
    margin-top: 15px;
}

.result.success {
    background: #d5f5e3;
    color: #27ae60;
}

.result.error {
    background: #fadbd8;
    color: #e74c3c;
}

.error-detail {
    margin-top: 8px;
    font-size: 14px;
    color: #7f8c8d;
}

ul {
    list-style: none;
    padding: 0;
}

ul li {
    padding: 8px 0;
    border-bottom: 1px solid #ecf0f1;
}

ul li:last-child {
    border-bottom: none;
}
</style>