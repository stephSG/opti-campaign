<template>
  <!--
    This component handles the UI and local state for the campaign form.
    It emits the filled data up to the parent view via the 'submitForm' event.
    English comments added for clarity and maintenance.
  -->
  <form @submit.prevent="handleSubmit" class="space-y-6 bg-white p-4 sm:p-6 md:p-8 rounded-lg shadow-md max-w-2xl mx-auto">

    <!-- Campaign Name -->
    <div>
      <label for="name" class="block text-sm font-medium text-gray-700">Campaign Name</label>
      <input
        type="text"
        id="name"
        v-model="formData.name"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        placeholder="e.g. Summer Sale 2025"
        aria-label="Campaign name"
      />
    </div>

    <!-- Description -->
    <div>
      <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
      <textarea
        id="description"
        v-model="formData.description"
        rows="4"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        placeholder="Briefly describe the campaign's goals"
        aria-label="Campaign description"
      ></textarea>
    </div>

    <!-- Date Pickers -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label for="start_date" class="block text-sm font-medium text-gray-700">Start Date</label>
        <input
          type="date"
          id="start_date"
          v-model="formData.start_date"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
          aria-label="Start date"
        />
      </div>
      <div>
        <label for="end_date" class="block text-sm font-medium text-gray-700">End Date</label>
        <input
          type="date"
          id="end_date"
          v-model="formData.end_date"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
          aria-label="End date"
        />
      </div>
    </div>

    <!-- Budget -->
    <div>
      <label for="budget" class="block text-sm font-medium text-gray-700">Budget ($)</label>
      <input
        type="number"
        id="budget"
        v-model.number="formData.budget"
        required
        min="0"
        step="0.01"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        placeholder="1000.00"
        aria-label="Budget"
      />
    </div>

    <!-- Status (Active) -->
    <div class="flex items-center">
      <input
        id="status"
        type="checkbox"
        v-model="formData.status"
        class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
        aria-label="Mark as active"
      />
      <label for="status" class="ml-2 block text-sm font-medium text-gray-900">Mark as Active</label>
    </div>

    <!-- Submission Buttons -->
    <!-- English comment: Buttons are grouped and responsive; primary action on the right. Icons improve affordance on small screens. -->
    <div class="flex flex-col sm:flex-row justify-end gap-3 pt-2">
      <router-link
        to="/"
        class="inline-flex items-center justify-center py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-200"
      >
        <!-- Cancel icon (X) -->
        <XMarkIcon class="h-4 w-4 mr-2 text-gray-500" />
        Cancel
      </router-link>

      <button
        type="submit"
        class="ml-0 sm:ml-3 inline-flex items-center justify-center py-2 px-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        <!-- Save icon (check) -->
        <CheckIcon class="h-4 w-4 mr-2" />
        Save Campaign
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue';
// Heroicons used in form buttons
import { CheckIcon, XMarkIcon } from '@heroicons/vue/24/outline';

// Define the component's props
const props = defineProps({
  campaignToEdit: {
    type: Object,
    default: null,
  },
});

// Define the event this component can emit
const emit = defineEmits(['submitForm']);

// Local reactive state for the form data
const formData = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  budget: 0,
  status: false,
});

/**
 * Helper function to format ISO date strings (from backend)
 * into "YYYY-MM-DD" format required by <input type="date">
 */
function formatDateForInput(dateString) {
  if (!dateString) return '';
  return new Date(dateString).toISOString().split('T')[0];
}

// Watch for changes to the 'campaignToEdit' prop and populate the form accordingly
watch(
  () => props.campaignToEdit,
  (newCampaign) => {
    if (newCampaign) {
      formData.value = {
        ...newCampaign,
        // Ensure dates are formatted correctly for the input fields
        start_date: formatDateForInput(newCampaign.start_date),
        end_date: formatDateForInput(newCampaign.end_date),
      };
    } else {
      // Reset form if in "New" mode (prop is null)
      formData.value = {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: 0,
        status: false,
      };
    }
  },
  { immediate: true } // Run the watcher immediately on component load
);

// Emits the form data to the parent component
const handleSubmit = () => {
  emit('submitForm', formData.value);
};
</script>
