<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <div class="container mx-auto p-4">

      <header class="flex flex-col sm:flex-row justify-between items-center py-4 mb-8 border-b border-purple-300 dark:border-purple-700">
        <h1 class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-4 sm:mb-0">
          Opti-Campaign 📈
        </h1>

        <nav class="space-x-4">
          <RouterLink
              to="/"
              class="text-lg font-medium text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400"
              active-class="text-purple-600 dark:text-purple-400"
          >
            Home
          </RouterLink>
          <RouterLink
              to="/login"
              class="text-lg font-medium text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400"
              active-class="text-purple-600 dark:text-purple-400"
          >
            Login
          </RouterLink>
        </nav>
      </header>

      <main>
        <RouterView v-slot="{ Component }">
          <template v-if="Component">
            <Transition name="fade" mode="out-in">
              <component :is="Component" />
            </Transition>
          </template>
        </RouterView>
      </main>

    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
// Auth logic (e.g., using Pinia) would be imported and managed here
// import { useAuthStore } from '@/stores/auth';
// const authStore = useAuthStore();
</script>

<style>
/* Simple fade transition for route changes */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
