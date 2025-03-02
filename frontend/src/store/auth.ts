import { defineStore } from 'pinia';
import api from '@/api/index';
import { jwtDecode } from 'jwt-decode';

interface User {
    id: number;
    email: string;
    username: string;
}

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || '',
        user: null as User | null
    }),

    getters: {
        isAuthenticated: (state): boolean => !!state.token
    },

    actions: {
        async login(credentials: { email: string; password: string }) {
            const data = await api
                .post('auth/login', { json: credentials })
                .json<{ access_token: string }>();

            this.token = data.access_token;
            this.user = jwtDecode(data.access_token) as User;
            localStorage.setItem('token', data.access_token);
        },

        logout() {
            this.token = '';
            this.user = null;
            localStorage.removeItem('token');
        }
    }
});
