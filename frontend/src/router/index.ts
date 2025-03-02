import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/store/auth';

const routes: Array<RouteRecordRaw> = [
    { path: '/', component: () => import('@/pages/Home.vue') },
    { path: '/login', component: () => import('@/pages/Login.vue') },
    {
        path: '/dashboard',
        component: () => import('@/pages/Dashboard.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/teams',
        component: () => import('@/pages/Teams.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/profile',
        component: () => import('@/pages/Profile.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/matches',
        component: () => import('@/pages/Matches.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/standings',
        component: () => import('@/pages/Standings.vue'),
        meta: { requiresAuth: true }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login');
    } else {
        next();
    }
});

export default router;
