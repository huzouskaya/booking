<template>
  <div id="app">
    <Header />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './stores/authStore';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

const authStore = useAuthStore();

onMounted(async () => {
  // Проверяем авторизацию при загрузке
  if (authStore.token && !authStore.user) {
    await authStore.fetchProfile();
  }
});
</script>

<style>
@import './styles/main.css';

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>