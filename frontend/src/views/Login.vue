<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>🔐 Вход в систему</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Имя пользователя</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Введите имя пользователя"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Введите пароль"
            required
          />
        </div>

        <button type="submit" :disabled="isLoading" class="btn-primary">
          {{ isLoading ? 'Вход...' : 'Войти' }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>

      <p class="auth-link">
        Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

const username = ref<string>('');
const password = ref<string>('');
const isLoading = ref<boolean>(false);
const error = ref<string>('');

const handleLogin = async (): Promise<void> => {
  isLoading.value = true;
  error.value = '';

  const result = await authStore.login(username.value, password.value);
  
  if (result.success) {
    await authStore.fetchProfile();
    router.push('/');
  } else {
    error.value = result.errors?.detail || 'Ошибка входа. Проверьте логин и пароль.';
  }

  isLoading.value = false;
};
</script>

<style scoped>
.auth-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f6fa;
}

.auth-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
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

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error {
  color: #e74c3c;
  margin-top: 10px;
  text-align: center;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  color: #7f8c8d;
}

.auth-link a {
  color: #3498db;
  text-decoration: none;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>