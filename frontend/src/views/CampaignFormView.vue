<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- English comment: Page title adjusts size on small screens and centers when narrow -->
    <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-6 text-center sm:text-left">{{ title }}</h1>

    <!-- Loading state while fetching campaign data for editing -->
    <div v-if="isLoading" class="text-center">
      <p class="text-gray-500">Loading campaign data...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="store.error && !campaignToEdit" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md" role="alert">
      <strong class="font-bold">Error:</strong>
      <span class="block sm:inline"> {{ store.error }}</span>
    </div>

    <!-- The CampaignForm component renders once data is ready -->
    <CampaignForm
      v-else
      :campaignToEdit="campaignToEdit"
      @submitForm="handleSubmit"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCampaignStore } from '../stores/campaignStore';
import CampaignForm from '../components/CampaignForm.vue';

// Initialize Vue Router and Pinia Store
const route = useRoute();
const router = useRouter();
const store = useCampaignStore();

// Get the campaign ID from the route parameters (will be undefined in "New" mode)
const campaignId = ref(route.params.id);
const isLoading = ref(false);

// Compute the title based on whether we are editing or creating
const title = computed(() => (campaignId.value ? 'Edit Campaign' : 'Create New Campaign'));

// Find the campaign in the store's state
const campaignToEdit = computed(() => {
  if (campaignId.value) {
    return store.campaigns.find((c) => c.id === parseInt(campaignId.value, 10));
  }
  return null;
});

// When the component mounts, fetch campaigns if needed (e.g., user landed directly on edit page)
onMounted(async () => {
  if (campaignId.value && !store.campaigns.length) {
    isLoading.value = true;
    await store.fetchCampaigns();
    isLoading.value = false;
  }
});

// Handle the form submission event from the CampaignForm component
const handleSubmit = async (formData) => {
  try {
    if (campaignId.value) {
      // Edit Mode: update existing campaign
      await store.updateCampaign(parseInt(campaignId.value, 10), formData);
    } else {
      // Create Mode: create new campaign
      await store.createCampaign(formData);
    }
    // On success, navigate back to the campaign list
    router.push('/');
  } catch (error) {
    console.error('Failed to save campaign:', error);
    // Store will carry the error; we avoid throwing UI-level exceptions here
  }
};
</script>
