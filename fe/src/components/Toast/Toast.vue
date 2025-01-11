<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'info', // 'info', 'success', 'error', 'warning'
  },
  visible: Boolean,
});

const emit = defineEmits(['close']);

const closeToast = () => {
  emit('close');
};

// Automatically close the toast after 3 seconds
watch(
  () => props.visible,
  (newVal) => {
    if (newVal) {
      setTimeout(() => {
        emit('close'); // Close toast after 3 seconds
      }, 3000);
    }
  },
  { immediate: true } // Make sure the effect is applied immediately when the component is mounted
);
</script>

<template>
  <div
    v-if="visible"
    class="fixed top-4 right-4 px-6 py-4 rounded-lg shadow-lg flex items-center space-x-3 z-50"
    :class="{
      'bg-green-500 text-white': type === 'success',
      'bg-red-500 text-white': type === 'error',
      'bg-yellow-500 text-black': type === 'warning',
      'bg-blue-500 text-white': type === 'info',
    }"
    @click="closeToast"
  >
    <p class="text-xl">{{ message }}</p> <!-- Increased font size -->
  </div>
</template>
