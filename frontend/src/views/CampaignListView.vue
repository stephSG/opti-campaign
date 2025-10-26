<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100">Campaigns</h1>
      <RouterLink
          to="/campaign/create"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
      >
        Create New Campaign
      </RouterLink>
    </div>

    <div v-if="loading" class="text-center text-gray-500 dark:text-gray-400">Loading campaigns...</div>
    <div v-if="error" class="text-center text-red-500">{{ error }}</div>

    <div v-if="!loading && !error && campaigns.length > 0" class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Name</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Budget</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Dates</th>
          <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
        </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
        <tr v-for="campaign in campaigns" :key="campaign.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium text-gray-900 dark:text-white">{{ campaign.name }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400 truncate max-w-xs">{{ campaign.description }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
              <span :class="statusClass(campaign.status)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                {{ campaign.status }}
              </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">${{ campaign.budget.toLocaleString() }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
            {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
            <button
                @click="handleToggleStatus(campaign)"
                class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300"
            >
              Toggle Status
            </button>
            <RouterLink :to="`/campaign/edit/${campaign.id}`" class="text-purple-600 hover:text-purple-900 dark:text-purple-400 dark:hover:text-purple-300">Edit</RouterLink>
            <button @click="handleDelete(campaign.id)" class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!loading && campaigns.length === 0" class="text-center text-gray-500 dark:text-gray-400 py-10">
      No campaigns found.
      <RouterLink to="/campaign/create" class="text-purple-600 hover:underline">Create one now</RouterLink>.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import api from '@/api/index.js'; // Assumes alias '@' is setup for '/src'

const campaigns = ref([]);
const loading = ref(true);
const error = ref(null);

const loadCampaigns = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await api.getCampaigns();
    campaigns.value = response.data;
  } catch (err) {
    console.error('Failed to load campaigns:', err);
    error.value = 'Failed to load campaigns. Please try again later.';
  } finally {
    loading.value = false;
  }
};

onMounted(loadCampaigns);

const handleDelete = async (id) => {
  if (confirm('Are you sure you want to delete this campaign?')) {
    try {
      await api.deleteCampaign(id);
      await loadCampaigns(); // Refresh the list
    } catch (err) {
      console.error('Failed to delete campaign:', err);
      alert('Failed to delete campaign.');
    }
  }
};

const handleToggleStatus = async (campaign) => {
  // Simple toggle logic, e.g., active <-> paused
  const newStatus = campaign.status === 'active' ? 'paused' : 'active';
  try {
    await api.updateCampaign(campaign.id, { ...campaign, status: newStatus });
    await loadCampaigns(); // Refresh the list
  } catch (err) {
    console.error('Failed to toggle status:', err);
    alert('Failed to toggle campaign status.');
  }
};

// --- Helper Functions ---

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString();
};

const statusClass = (status) => {
  switch (status) {
    case 'active':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100';
    case 'paused':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100';
    case 'completed':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100';
    case 'draft':
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-100';
  }
};
</script>
