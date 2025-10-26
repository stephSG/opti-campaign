<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6 text-center">
      {{ title }}
    </h1>

    <!-- Loading state while fetching campaign data for editing -->
    <div v-if="isLoading" class="text-center">
      <p>Loading campaign data...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="store.error && !campaignToEdit" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md" role="alert">
      <strong class="font-bold">Error:</strong>
      <span class="block sm:inline"> {{ store.error }}</span>
    </div>

    <!--
      The form component is rendered once data is ready.
      - :campaignToEdit="campaignToEdit" -> Passes the loaded data (or null) as a prop
      - @submitForm="handleSubmit"      -> Listens for the custom event from the component
    -->
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

// When the component mounts, check if we need to fetch data
onMounted(async () => {
  if (campaignId.value && !store.campaigns.length) {
    // If we are in "Edit" mode and the store is empty
    // (e.g., user reloaded on the edit page), fetch all campaigns.
    isLoading.value = true;
    await store.fetchCampaigns();
    isLoading.value = false;
  }
});

// Handle the form submission event from the CampaignForm component
const handleSubmit = async (formData) => {
  try {
    if (campaignId.value) {
      // --- Edit Mode ---
      // We pass the ID and the form data to the store's update action
      await store.updateCampaign(parseInt(campaignId.value, 10), formData);
    } else {
      // --- Create Mode ---
      await store.createCampaign(formData);
    }
    // On success, navigate back to the campaign list
    router.push('/');
  } catch (error) {
    console.error('Failed to save campaign:', error);
    // Error is already set in the store, we could show a modal here
  }
};
</script>
