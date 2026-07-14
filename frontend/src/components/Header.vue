<template>
    <header class="header">
        <div class="header-container">
        <router-link to="/" class="logo">
            <span class="logo-icon">🏫</span>
            <span class="logo-text">Бронирование</span>
        </router-link>

        <nav class="nav-links">
            <router-link to="/" class="nav-link">Главная</router-link>
            <router-link to="/resources" class="nav-link">Ресурсы</router-link>

            <template v-if="authStore.isAuthenticated">
            <router-link to="/bookings" class="nav-link">Мои бронирования</router-link>
            <router-link v-if="authStore.isAdmin" to="/admin" class="nav-link admin-link">
                Админка
            </router-link>

            <div class="user-menu">
                <span class="user-name">{{ authStore.userName }}</span>
                <button @click="handleLogout" class="logout-btn">Выйти</button>
            </div>
            </template>

            <template v-else>
            <router-link to="/login" class="nav-link">Войти</router-link>
            <router-link to="/register" class="nav-link register-link">Регистрация</router-link>
            </template>
        </nav>
        </div>
    </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();

const handleLogout = (): void => {
    if (confirm('Вы уверены, что хотите выйти?')) {
        authStore.logout();
    }
};
</script>

<style scoped>
.header {
    background: #2c3e50;
    color: white;
    padding: 0 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: white;
    font-weight: bold;
    font-size: 1.3rem;
}

.logo-icon {
    font-size: 1.8rem;
}

.logo-text {
    color: white;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 20px;
}

.nav-link {
    color: rgba(255,255,255,0.8);
    text-decoration: none;
    padding: 6px 12px;
    border-radius: 4px;
    transition: all 0.2s;
    font-size: 0.95rem;
}

.nav-link:hover {
    color: white;
    background: rgba(255,255,255,0.1);
}

.nav-link.router-link-active {
    color: white;
    background: rgba(255,255,255,0.15);
}

.admin-link {
    color: #f1c40f !important;
}

.admin-link:hover {
    background: rgba(241, 196, 15, 0.2) !important;
}

.register-link {
    background: #3498db;
    color: white !important;
    padding: 6px 16px;
    border-radius: 6px;
}

.register-link:hover {
    background: #2980b9 !important;
    color: white !important;
}

.user-menu {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-left: 12px;
    border-left: 1px solid rgba(255,255,255,0.2);
}

.user-name {
    color: rgba(255,255,255,0.9);
    font-size: 0.95rem;
}

.logout-btn {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 5px 14px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.2s;
}

.logout-btn:hover {
    background: #c0392b;
}

@media (max-width: 768px) {
    .header-container {
        flex-direction: column;
        height: auto;
        padding: 12px 0;
    }

    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-top: 8px;
    }

    .user-menu {
        border-left: none;
        padding-left: 0;
    }
}
</style>