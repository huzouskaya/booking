<template>
    <div class="auth-container">
        <div class="auth-card">
            <h2>📝 Регистрация</h2>
            
            <form @submit.prevent="handleRegister">
                <div class="form-group">
                    <label for="username">Имя пользователя</label>
                    <input
                        id="username"
                        v-model="form.username"
                        type="text"
                        placeholder="Введите имя пользователя"
                        required
                    />
                </div>

                <div class="form-group">
                    <label for="email">Email</label>
                    <input
                        id="email"
                        v-model="form.email"
                        type="email"
                        placeholder="Введите email"
                        required
                    />
                </div>

                <div class="form-group">
                    <label for="first_name">Имя</label>
                    <input
                        id="first_name"
                        v-model="form.first_name"
                        type="text"
                        placeholder="Введите ваше имя"
                    />
                </div>

                <div class="form-group">
                    <label for="last_name">Фамилия</label>
                    <input
                        id="last_name"
                        v-model="form.last_name"
                        type="text"
                        placeholder="Введите вашу фамилию"
                    />
                </div>

                <div class="form-group">
                    <label for="password">Пароль</label>
                    <input
                        id="password"
                        v-model="form.password"
                        type="password"
                        placeholder="Введите пароль"
                        required
                    />
                </div>

                <div class="form-group">
                    <label for="password2">Подтверждение пароля</label>
                    <input
                        id="password2"
                        v-model="form.password2"
                        type="password"
                        placeholder="Подтвердите пароль"
                        required
                    />
                </div>

                <div class="form-group">
                    <label for="role">Роль</label>
                    <select id="role" v-model="form.role">
                        <option value="user">Пользователь</option>
                        <option value="teacher">Преподаватель</option>
                    </select>
                </div>

                <button type="submit" :disabled="isLoading" class="btn-primary">
                {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
                </button>

                <p v-if="error" class="error">{{ error }}</p>
                <p v-if="success" class="success">Регистрация успешна! Перенаправляем...</p>
            </form>

            <p class="auth-link">
                Уже есть аккаунт? <router-link to="/login">Войти</router-link>
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password2: '',
    role: 'user'
});

const isLoading = ref(false);
const error = ref('');
const success = ref(false);

const handleRegister = async () => {
    isLoading.value = true;
    error.value = '';
    success.value = false;

    const result = await authStore.register(form);
    
    if (result.success) {
        success.value = true;
        setTimeout(() => {
        router.push('/');
        }, 1500);
    } else {
        const errors = result.errors;
        if (errors.username) error.value = errors.username[0];
        else if (errors.password) error.value = errors.password[0];
        else if (errors.email) error.value = errors.email[0];
        else error.value = result.errors.detail || 'Ошибка регистрации';
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

.form-group input,
.form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
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

.success {
    color: #27ae60;
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