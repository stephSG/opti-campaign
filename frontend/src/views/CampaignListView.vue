<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Header: page title and primary action -->
    <!-- English comment: Responsive header with title on the left and create button on the right. On narrow screens the elements wrap. -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Campaigns</h1>
      <router-link
        to="/campaign/new"
        class="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        <!-- Plus icon -->
        <PlusIcon class="h-4 w-4" />
        Create New Campaign
      </router-link>
    </div>

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="text-center py-10">
      <p class="text-gray-500">Loading campaigns...</p>
      <!-- You could add a spinner SVG here -->
    </div>

    <!-- Error Message -->
    <div v-else-if="store.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md" role="alert">
      <strong class="font-bold">Error:</strong>
      <span class="block sm:inline"> {{ store.error }}</span>
    </div>

    <!-- Campaign Table (Desktop) -->
    <!-- English comment: We hide the table on small screens and show it on md+ screens. Table uses compact classes for better readability. -->
    <div v-else-if="campaigns.length > 0" class="hidden md:block bg-white shadow-sm rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200 table-fixed">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
            <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Budget</th>
            <th scope="col" class="relative px-4 py-3"><span class="sr-only">Actions</span></th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="campaign in campaigns" :key="campaign.id" class="hover:bg-gray-50">
            <td class="px-4 py-4 whitespace-nowrap max-w-xs">
              <div class="text-sm font-medium text-gray-900 truncate">{{ campaign.name }}</div>
              <div class="text-sm text-gray-500 truncate">{{ campaign.description }}</div>
            </td>
            <td class="px-4 py-4 whitespace-nowrap">
              <span :class="campaign.status ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                {{ campaign.status ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}
            </td>
            <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">${{ campaign.budget.toLocaleString() }}</td>
            <!-- Actions: use icon buttons with sr-only labels for accessibility -->
            <td class="px-4 py-4 whitespace-nowrap text-right text-sm font-medium flex items-center justify-end gap-2">
              <IconButton
                :icon="campaign.status ? CheckIcon : XMarkIcon"
                :label="campaign.status ? 'Deactivate' : 'Activate'"
                @click="handleToggle(campaign)"
                class="text-gray-500 hover:text-gray-700"
              />

              <router-link :to="{ name: 'Edit', params: { id: campaign.id } }" class="p-2 rounded-md text-indigo-600 hover:text-indigo-900 hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-200" title="Edit">
                <span class="sr-only">Edit</span>
                <!-- Pencil icon -->
                <PencilSquareIcon class="h-5 w-5" />
              </router-link>

              <IconButton
                :icon="TrashIcon"
                label="Delete"
                variant="danger"
                @click="handleDelete(campaign.id)"
                class="text-red-600 hover:text-red-900"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Campaign Cards (Mobile) -->
    <!-- English comment: Compact card layout for small screens. Action icons are grouped and wrap when space is limited. -->
    <div v-else-if="campaigns.length > 0" class="md:hidden space-y-4">
      <div v-for="campaign in campaigns" :key="campaign.id" class="bg-white shadow-sm rounded-lg p-4">
        <div class="flex justify-between items-start gap-3">
          <div class="flex-1">
            <h2 class="text-lg font-semibold text-gray-900 truncate">{{ campaign.name }}</h2>
            <p class="text-sm text-gray-600 mt-1 truncate">{{ campaign.description }}</p>
            <div class="mt-2 flex items-center gap-3 text-sm text-gray-500">
              <span class="inline-flex items-center gap-2">
                <strong class="text-gray-700">Budget:</strong>
                ${{ campaign.budget.toLocaleString() }}
              </span>
              <span class="inline-flex items-center gap-2">
                <strong class="text-gray-700">Duration:</strong>
                {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}
              </span>
            </div>
          </div>

          <div class="flex-shrink-0 ml-2 flex flex-col items-end gap-2">
            <span :class="campaign.status ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
              {{ campaign.status ? 'Active' : 'Inactive' }}
            </span>

            <div class="mt-2 flex items-center gap-2">
              <IconButton
                :icon="campaign.status ? CheckIcon : XMarkIcon"
                :label="campaign.status ? 'Deactivate' : 'Activate'"
                @click="handleToggle(campaign)"
                class="text-gray-500 hover:text-gray-700"
              />

              <router-link :to="{ name: 'Edit', params: { id: campaign.id } }" class="p-2 rounded-md text-indigo-600 hover:text-indigo-900 hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-200" title="Edit">
                <span class="sr-only">Edit</span>
                <PencilSquareIcon class="h-5 w-5" />
              </router-link>

              <IconButton
                :icon="TrashIcon"
                label="Delete"
                variant="danger"
                @click="handleDelete(campaign.id)"
                class="text-red-600 hover:text-red-900"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-10 bg-white rounded-lg shadow-sm">
      <h3 class="mt-2 text-lg font-medium text-gray-900">No campaigns found</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by creating a new campaign.</p>
      <div class="mt-4">
        <router-link to="/campaign/new" class="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
          <PlusIcon class="h-4 w-4" />
          Create Campaign
        </router-link>
      </div>
    </div>
  </div>

  <!-- Confirm modal (rendered outside the v-if / v-else-if chain so it doesn't break the conditional rendering) -->
  <ConfirmModal
    v-if="modalVisible"
    :title="modalTitle"
    :message="modalMessage"
    @confirm="onModalConfirm"
    @cancel="onModalCancel"
  />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useCampaignStore } from '../stores/campaignStore';
// Import Heroicons and reusable IconButton
import { PlusIcon, PencilSquareIcon, TrashIcon, CheckIcon, XMarkIcon } from '@heroicons/vue/24/outline';
import IconButton from '../components/IconButton.vue';
import ConfirmModal from '../components/ConfirmModal.vue';

// Initialize the store
const store = useCampaignStore();

// Computed state properties
const campaigns = computed(() => store.campaigns);
const isLoading = computed(() => store.isLoading);

// Modal state for confirmation dialog
const modalVisible = ref(false);
const modalMessage = ref('');
const modalTitle = ref('Confirm');
let modalResolve = null;

// Helper that opens the confirm modal and returns a Promise resolved with a boolean
function requestConfirm(message, title = 'Confirm') {
  modalMessage.value = message;
  modalTitle.value = title;
  modalVisible.value = true;
  return new Promise((resolve) => {
    modalResolve = resolve;
  });
}

function onModalConfirm() {
  modalVisible.value = false;
  if (modalResolve) modalResolve(true);
  modalResolve = null;
}

function onModalCancel() {
  modalVisible.value = false;
  if (modalResolve) modalResolve(false);
  modalResolve = null;
}

// Fetch campaigns on mount
onMounted(() => {
  store.fetchCampaigns();
});

// --- Methods ---
// Helper to format dates for display (English comment)
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

// Handle delete with confirmation
const handleDelete = async (id) => {
  const confirmed = await requestConfirm('Are you sure you want to delete this campaign?', 'Delete campaign');
  if (confirmed) {
    await store.deleteCampaign(id);
  }
};

// Handle toggle (activate/deactivate) with confirmation
const handleToggle = async (campaign) => {
  const action = campaign.status ? 'deactivate' : 'activate';
  const confirmed = await requestConfirm(`Are you sure you want to ${action} this campaign?`, `${action[0].toUpperCase() + action.slice(1)} campaign`);
  if (confirmed) {
    await store.toggleCampaign(campaign.id);
  }
};
</script>
