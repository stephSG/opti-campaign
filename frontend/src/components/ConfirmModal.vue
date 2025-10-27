<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center" aria-modal="true" role="dialog">
    <div class="fixed inset-0 bg-black/50" @click="onCancel"></div>
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full mx-4 p-6 z-10">
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
      <p class="text-sm text-gray-600 mb-4">{{ message }}</p>
      <div class="flex justify-end gap-3">
        <button @click="onCancel" class="px-3 py-2 rounded-md border border-gray-300 bg-white text-sm">Cancel</button>
        <button data-test="confirm-ok" @click="onConfirm" class="px-3 py-2 rounded-md bg-red-600 text-white text-sm">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, default: 'Confirm' },
  message: { type: String, required: true },
});

const emit = defineEmits(['confirm', 'cancel']);

const onConfirm = () => emit('confirm');
const onCancel = () => emit('cancel');
</script>

