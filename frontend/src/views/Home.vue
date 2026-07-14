<template>
  <div class="home">
    <header>
      <h1>🏫 Система бронирования</h1>
      <p class="subtitle">Бронируйте аудитории и оборудование онлайн</p>
    </header>

    <div class="features">
      <div class="feature-card" @click="$router.push('/resources')">
        <span class="icon">📚</span>
        <h3>Каталог ресурсов</h3>
        <p>Просматривайте доступные аудитории, классы и оборудование</p>
      </div>

      <div class="feature-card" @click="$router.push('/resources')">
        <span class="icon">📅</span>
        <h3>Бронирование</h3>
        <p>Бронируйте ресурсы на удобное время с проверкой доступности</p>
      </div>

      <div class="feature-card" @click="$router.push('/bookings')">
        <span class="icon">📋</span>
        <h3>Мои бронирования</h3>
        <p>Просматривайте и управляйте своими заявками</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Главная страница — без логики
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

header {
  text-align: center;
  margin-bottom: 50px;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.feature-card .icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 15px;
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.feature-card p {
  color: #7f8c8d;
  margin: 0;
}
</style>