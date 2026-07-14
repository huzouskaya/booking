import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { useAuthStore } from './stores/authStore';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// 🔥 Восстанавливаем сессию при загрузке приложения
const authStore = useAuthStore();
if (authStore.isAuthenticated) {
    // Если есть токен в localStorage, загружаем профиль
    authStore.fetchProfile().catch(() => {
        // Если профиль не загрузился — выходим
        authStore.logout();
    });
}

app.mount('#app');