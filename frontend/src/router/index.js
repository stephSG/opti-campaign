import { createRouter, createWebHistory } from 'vue-router';

// 2. Import views
// Assuming views are in ../views/ as per the file map
import CampaignListView from '../views/CampaignListView.vue';
import CampaignFormView from '../views/CampaignFormView.vue';
import LoginView from '../views/LoginView.vue';

// 3. Define routes
const routes = [
    {
        path: '/',
        name: 'campaign-list',
        component: CampaignListView,
        meta: { requiresAuth: true }
    },
    {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: { guest: true } // For users who are NOT logged in
    },
    {
        path: '/campaign/create',
        name: 'campaign-create',
        component: CampaignFormView,
        meta: { requiresAuth: true }
    },
    {
        path: '/campaign/edit/:id',
        name: 'campaign-edit',
        component: CampaignFormView,
        props: true, // Pass route params (e.g., :id) as component props
        meta: { requiresAuth: true }
    }
];

// 1. Use createRouter and createWebHistory
const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 4. Implement router.beforeEach navigation guard
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token'); // Check for token (or from Pinia store)

    if (to.meta.requiresAuth && !token) {
        // This route requires auth, but user is not logged in
        next({ name: 'login' });
    } else if (to.meta.guest && token) {
        // This route (login) is for guests, but user is already logged in
        next({ name: 'campaign-list' });
    } else {
        // All good
        next();
    }
});

export default router;
