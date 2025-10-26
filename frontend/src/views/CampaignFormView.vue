<template>
  <div class="max-w-4xl mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">
      {{ isEdit ? 'Edit Campaign' : 'Create New Campaign' }}
    </h1>

    <div v-if="loading" class="text-center text-gray-500 dark:text-gray-400">Loading campaign data...</div>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline"> {{ error }}</span>
    </div>

    <CampaignForm
        v-if="!loading"
        :isEdit="isEdit"
        :campaignData="campaignData"
        @submit="handleSubmit"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CampaignForm from '@/components/CampaignForm.vue'; // Assumes alias '@' is setup for '/src'
import api from '@/api/index.js';

const route = useRoute();
const router = useRouter();

const campaignData = ref({});
const isEdit = ref(false);
const loading = ref(false);
const error = ref(null);

const campaignId = route.params.id;

onMounted(async () => {
  if (campaignId) {
    isEdit.value = true;
    loading.value = true;
    try {
      const response = await api.getCampaign(campaignId);
      campaignData.value = response.data;
    } catch (err) {
      console.error('Failed to fetch campaign data:', err);
      error.value = 'Could not load campaign data for editing.';
    } finally {
      loading.value = false;
    }
  }
});

const handleSubmit = async (formData) => {
  error.value = null; // Clear previous errors
  try {
    if (isEdit.value) {
      // Update existing campaign
      await api.updateCampaign(campaignId, formData);
    } else {
      // Create new campaign
      await api.createCampaign(formData);
    }
    // On success, navigate back to the list view
    router.push('/');
  } catch (err) {
    console.error('Failed to save campaign:', err);
    error.value = 'Failed to save campaign. Please check the form and try again.';
  }
};
</script>
