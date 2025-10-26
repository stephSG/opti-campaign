<template>
  <form @submit.prevent="handleSubmit" class="space-y-6 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">

    <div>
      <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Campaign Name</label>
      <input
          type="text"
          id="name"
          v-model="form.name"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
      />
    </div>

    <div>
      <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Description</label>
      <textarea
          id="description"
          v-model="form.description"
          rows="3"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
      ></textarea>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="start_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Start Date</label>
        <input
            type="date"
            id="start_date"
            v-model="form.start_date"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
        />
      </div>
      <div>
        <label for="end_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">End Date</label>
        <input
            type="date"
            id="end_date"
            v-model="form.end_date"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
        />
      </div>
    </div>

    <div>
      <label for="budget" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Budget ($)</label>
      <input
          type="number"
          id="budget"
          v-model.number="form.budget"
          required
          min="0"
          step="0.01"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
      />
    </div>

    <div>
      <label for="status" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
      <select
          id="status"
          v-model="form.status"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 bg-white dark:bg-gray-700 dark:text-white"
      >
        <option value="draft">Draft</option>
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <div class="flex justify-end">
      <button
          type="submit"
          class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
      >
        {{ isEdit ? 'Update Campaign' : 'Create Campaign' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, watchEffect } from 'vue';

// 1. Define Props
const props = defineProps({
  campaignData: {
    type: Object,
    default: () => ({})
  },
  isEdit: {
    type: Boolean,
    default: false
  }
});

// 2. Define Emits
const emit = defineEmits(['submit']);

// 3. Define Form Model
const form = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  budget: 0,
  status: 'draft'
});

// Helper function to format date for input type="date" (YYYY-MM-DD)
const formatDateForInput = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toISOString().split('T')[0];
};

// 4. Watch for prop changes to update the form (for editing)
watchEffect(() => {
  if (props.isEdit && props.campaignData) {
    form.value = {
      ...props.campaignData,
      start_date: formatDateForInput(props.campaignData.start_date),
      end_date: formatDateForInput(props.campaignData.end_date),
    };
  } else {
    // Reset form for creation
    form.value = {
      name: '',
      description: '',
      start_date: '',
      end_date: '',
      budget: 0,
      status: 'draft'
    };
  }
});

// 5. Handle Form Submission
const handleSubmit = () => {
  // Emit the form data to the parent view
  emit('submit', { ...form.value });
};
</script>
