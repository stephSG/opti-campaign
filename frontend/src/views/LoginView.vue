<template>
  <div class="max-w-md mx-auto mt-10">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-purple-600 dark:text-purple-400">
        Login to Opti-Campaign
      </h2>

      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Username
          </label>
          <input
            type="text"
            id="username"
            v-model="credentials.username"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
            placeholder="Enter your username"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Password
          </label>
          <input
            type="password"
            id="password"
            v-model="credentials.password"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
            placeholder="Enter your password"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <div class="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
        <p>Demo credentials:</p>
        <p class="font-mono text-xs mt-2">
          Username: <strong>admin</strong> / Password: <strong>admin123</strong>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api/index.js';

const router = useRouter();

const credentials = ref({
  username: '',
  password: ''
});

const loading = ref(false);
const error = ref(null);

const handleLogin = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await api.login(credentials.value);

    // Store the token
    if (response.data && response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      // Redirect to home page
      router.push('/');
    } else {
      error.value = 'Invalid response from server';
    }
  } catch (err) {
    console.error('Login failed:', err);
    if (err.response?.status === 401) {
      error.value = 'Invalid username or password';
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail;
    } else {
      error.value = 'Login failed. Please check if the backend server is running.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

