import { createRouter, createWebHistory } from 'vue-router';
import { useCampaignStore } from '../stores/campaignStore';

// Import views
// We use dynamic imports (lazy loading) for better performance
const CampaignListView = () => import('../views/CampaignListView.vue');
const CampaignFormView = () => import('../views/CampaignFormView.vue');
const LoginView = () => import('../views/LoginView.vue');

const routes = [
    {
        path: '/',
        name: 'List',
        component: CampaignListView,
        meta: { requiresAuth: true }, // This route requires authentication
    },
    {
        path: '/campaign/new',
        name: 'New',
        component: CampaignFormView,
        meta: { requiresAuth: true },
    },
    {
        path: '/campaign/edit/:id',
        name: 'Edit',
        component: CampaignFormView,
        props: true, // Passes route.params.id as a prop to the component
        meta: { requiresAuth: true },
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
        meta: { requiresAuth: false }, // This route does not require auth
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

/**
 * Navigation Guard:
 * This runs before each navigation.
 */
router.beforeEach((to, from, next) => {
    // We must initialize the store *inside* the guard
    // to ensure it's available.
    const store = useCampaignStore();

    const isAuthenticated = store.isAuthenticated;
    const requiresAuth = to.meta.requiresAuth;

    if (requiresAuth && !isAuthenticated) {
        // If route requires auth and user is not logged in, redirect to login
        next({ name: 'Login' });
    } else if (to.name === 'Login' && isAuthenticated) {
        // If user is logged in and tries to access login page, redirect to home
        next({ name: 'List' });
    } else {
        // Otherwise, proceed
        next();
    }
});

export default router;
