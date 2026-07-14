import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Resources from '../views/Resources.vue';
import ResourceDetail from '../views/ResourceDetail.vue';
import MyBookings from '../views/MyBookings.vue';
import CreateBooking from '../views/CreateBooking.vue';
import AdminPanel from '../views/AdminPanel.vue';
import SeedData from '../views/SeedData.vue';

const routes: RouteRecordRaw[] = [
    { path: '/', name: 'Home', component: Home },
    { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
    { path: '/register', name: 'Register', component: Register, meta: { guest: true } },
    { path: '/resources', name: 'Resources', component: Resources },
    { path: '/resources/:id', name: 'ResourceDetail', component: ResourceDetail },
    { path: '/bookings', name: 'MyBookings', component: MyBookings, meta: { requiresAuth: true } },
    { path: '/bookings/create', name: 'CreateBooking', component: CreateBooking, meta: { requiresAuth: true } },
    { path: '/admin', name: 'AdminPanel', component: AdminPanel, meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/seed', name: 'SeedData', component: SeedData },  // Доступен всем
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from) => {
    const authStore = useAuthStore();

    if (authStore.token && !authStore.user) {
        await authStore.fetchProfile();
    }

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        return '/login';
    }

    if (to.meta.requiresAdmin && !authStore.isAdmin) {
        return '/';
    }

    if (to.meta.guest && authStore.isAuthenticated) {
        return '/';
    }
    
    return true;
});

export default router;