<!--
================================================================================
 Component: Toast.vue
 Description:
        Toast notification component for displaying messages about action results.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'info',
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
        emit('close'); 
      }, 3000);
    }
  },
  { immediate: true }
);
</script>

<template>

  <div
    v-if="visible"
    class="fixed top-4 left-1/2 transform -translate-x-1/2 px-6 py-4 rounded-lg shadow-lg flex items-center space-x-3 z-50"
    :class="{
      'bg-green-500 text-white': type === 'success',
      'bg-red-500 text-white': type === 'error',
      'bg-yellow-500 text-black': type === 'warning',
      'bg-blue-500 text-white': type === 'info',
    }"
    @click="closeToast">

    <p class="text-xl">{{ message }}</p>

  </div>

</template>

