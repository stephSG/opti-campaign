<template>
  <!--
    Reusable icon button component.
    Props:
      - icon: component to render (Heroicons or other)
      - label: accessible label (string)
      - variant: optional style variant (e.g. 'danger')
      - size: tailwind size classes (default 'h-5 w-5')
    Usage:
      <IconButton :icon="TrashIcon" label="Delete" variant="danger" @click="onDelete" />
  -->
  <button
    :class="buttonClass"
    @click="$emit('click')"
    :title="label"
    type="button"
  >
    <component :is="icon" :class="iconClass" aria-hidden="true" />
    <span class="sr-only">{{ label }}</span>
  </button>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
  icon: { type: [Object, Function], required: true },
  label: { type: String, required: true },
  variant: { type: String, default: 'default' },
  size: { type: String, default: 'h-5 w-5' },
});

const iconClass = computed(() => `${props.size}`);

const buttonClass = computed(() => {
  const base = 'p-2 rounded-md focus:outline-none';
  if (props.variant === 'danger') return `${base} text-red-600 hover:text-red-900 hover:bg-red-50 focus:ring-2 focus:ring-red-200`;
  if (props.variant === 'primary') return `${base} text-indigo-600 hover:text-indigo-900 hover:bg-indigo-50 focus:ring-2 focus:ring-indigo-200`;
  if (props.variant === 'success') return `${base} text-green-600 hover:text-green-900 hover:bg-green-50 focus:ring-2 focus:ring-green-200`;
  return `${base} text-gray-500 hover:text-gray-700 hover:bg-gray-50 focus:ring-2 focus:ring-indigo-200`;
});

const emit = defineEmits(['click']);
</script>

