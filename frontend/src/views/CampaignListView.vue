<template>
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Campaigns</h1>
      <router-link
          to="/campaign/new"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Create New Campaign
      </router-link>
    </div>

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="text-center py-10">
      <p class="text-gray-500">Loading campaigns...</p>
      <!-- You could add a spinner SVG here -->
    </div>

    <!-- Error Message -->
    <div v-else-if="store.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md" role="alert">
      <strong class="font-bold">Error:</strong>
      <span class="block sm:inline"> {{ store.error }}</span>
    </div>

    <!-- Campaign Table (Desktop) -->
    <div v-else-if="campaigns.length > 0" class="hidden md:block bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Budget</th>
          <th scope="col" class="relative px-6 py-3"><span class="sr-only">Actions</span></th>
        </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="campaign in campaigns" :key="campaign.id">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium text-gray-900">{{ campaign.name }}</div>
            <div class="text-sm text-gray-500 truncate max-w-xs">{{ campaign.description }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
              <span
                  :class="campaign.status ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
              >
                {{ campaign.status ? 'Active' : 'Inactive' }}
              </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${{ campaign.budget.toLocaleString() }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
            <button @click="handleToggle(campaign)" class="text-gray-500 hover:text-gray-700" :title="campaign.status ? 'Deactivate' : 'Activate'">
              <!-- Simple Toggle Icon (Replace with SVG icons later) -->
              {{ campaign.status ? 'Deactivate' : 'Activate' }}
            </button>
            <router-link :to="{ name: 'Edit', params: { id: campaign.id } }" class="text-indigo-600 hover:text-indigo-900">Edit</router-link>
            <button @click="handleDelete(campaign.id)" class="text-red-600 hover:text-red-900">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Campaign Cards (Mobile) -->
    <div v-else-if="campaigns.length > 0" class="md:hidden space-y-4">
      <div v-for="campaign in campaigns" :key="campaign.id" class="bg-white shadow-md rounded-lg p-4">
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-lg font-semibold text-gray-900">{{ campaign.name }}</h2>
          <span
              :class="campaign.status ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
              class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
          >
              {{ campaign.status ? 'Active' : 'Inactive' }}
            </span>
        </div>
        <p class="text-sm text-gray-600 mb-3">{{ campaign.description }}</p>
        <div class="border-t border-gray-200 pt-3">
          <p class="text-sm text-gray-500"><strong>Budget:</strong> ${{ campaign.budget.toLocaleString() }}</p>
          <p class="text-sm text-gray-500"><strong>Duration:</strong> {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}</p>
        </div>
        <div class="flex justify-end space-x-2 mt-4">
          <button @click="handleToggle(campaign)" class="text-sm text-gray-500 hover:text-gray-700">
            {{ campaign.status ? 'Deactivate' : 'Activate' }}
          </button>
          <router-link :to="{ name: 'Edit', params: { id: campaign.id } }" class="text-sm text-indigo-600 hover:text-indigo-900">Edit</router-link>
          <button @click="handleDelete(campaign.id)" class="text-sm text-red-600 hover:text-red-900">Delete</button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-10 bg-white rounded-lg shadow-md">
      <h3 class="mt-2 text-lg font-medium text-gray-900">No campaigns found</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by creating a new campaign.</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useCampaignStore } from '../stores/campaignStore';

// Initialize the store
const store = useCampaignStore();

// Create computed properties to reactively access state
const campaigns = computed(() => store.campaigns);
const isLoading = computed(() => store.isLoading);

// Fetch campaigns when the component is first mounted
onMounted(() => {
  store.fetchCampaigns();
});

// --- Methods ---

// Helper to format dates
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

// Handle the delete action
const handleDelete = async (id) => {
  if (confirm('Are you sure you want to delete this campaign?')) {
    await store.deleteCampaign(id);
    // No need to re-fetch, store handles optimistic update
  }
};

// Handle the toggle action
const handleToggle = async (campaign) => {
  const action = campaign.status ? 'deactivate' : 'activate';
  if (confirm(`Are you sure you want to ${action} this campaign?`)) {
    await store.toggleCampaign(campaign.id);
  }
};
</script>
