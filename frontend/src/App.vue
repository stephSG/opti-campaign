<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Main Navigation Bar -->
    <nav v-if="isLoggedIn" class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo/Title -->
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="text-2xl font-bold text-indigo-600">
              Opti-Campaign
            </router-link>
          </div>

          <!-- Logout Button -->
          <div class="flex items-center">
            <button
                @click="handleLogout"
                class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-600 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="py-8">
      <!-- RouterView renders the component for the current route -->
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue';
// FIXED: Corrected the import statement below
import { RouterView, RouterLink, useRouter } from 'vue-router';
import { useCampaignStore } from './stores/campaignStore';

const store = useCampaignStore();
const router = useRouter();

// Computed property to check if the user is logged in
const isLoggedIn = computed(() => store.isAuthenticated);

// Logout action
const handleLogout = () => {
  store.logout();
  // Redirect to the login page after logging out
  router.push('/login');
};
</script>

