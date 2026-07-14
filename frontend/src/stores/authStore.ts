import { defineStore } from 'pinia';
import api from '../services/api';
import type { User, RegisterData, AuthResponse } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    isAuthenticated: !!localStorage.getItem('access_token'),
    loading: false,
  }),

  actions: {
    async register(userData: RegisterData) {
      this.loading = true;
      try {
        const response = await api.post<AuthResponse>('users/register/', userData);
        const { user, access, refresh } = response.data;
        
        this.user = user;
        this.token = access;
        this.isAuthenticated = true;
        
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        
        this.loading = false;
        return { success: true, user };
      } catch (error: any) {
        this.loading = false;
        return { success: false, errors: error.response?.data };
      }
    },

    async login(username: string, password: string) {
      this.loading = true;
      try {
        const response = await api.post('users/token/', { username, password });
        const { access, refresh } = response.data;
        
        this.token = access;
        this.isAuthenticated = true;
        
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        
        await this.fetchProfile();
        this.loading = false;
        return { success: true };
      } catch (error: any) {
        this.loading = false;
        return { success: false, errors: error.response?.data };
      }
    },

    async fetchProfile() {
      try {
        const response = await api.get<User>('users/profile/');
        this.user = response.data;
        this.isAuthenticated = true;
        return response.data;
      } catch (error) {
        this.logout();
        return null;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      this.loading = false;
      
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    },

    async refreshToken() {
      try {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) throw new Error('No refresh token');
        
        const response = await api.post('users/token/refresh/', { refresh });
        const { access } = response.data;
        
        this.token = access;
        localStorage.setItem('access_token', access);
        return access;
      } catch (error) {
        this.logout();
        throw error;
      }
    }
  },

  getters: {
    isAdmin: (state) => state.user?.role === 'admin' || state.user?.is_staff === true,
    isTeacher: (state) => state.user?.role === 'teacher',
    isUser: (state) => state.user?.role === 'user',
    userName: (state) => state.user?.first_name || state.user?.username || 'Гость',
  }
});