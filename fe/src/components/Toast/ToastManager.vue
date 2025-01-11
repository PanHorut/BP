<script setup>
import { ref } from 'vue';
import Toast from './Toast.vue';

const toasts = ref([]);

// Function to show a toast
const showToast = (message, type = 'info') => {
  const newToast = {
    message,
    type,
    visible: true,
  };
  toasts.value.push(newToast);
};

// Function to remove a toast by index
const removeToast = (index) => {
  toasts.value.splice(index, 1);
};

defineExpose({ showToast });

</script>

<template>
  <div>
    <!-- Loop through toasts and display them -->
    <Toast
      v-for="(toast, index) in toasts"
      :key="index"
      :message="toast.message"
      :type="toast.type"
      :visible="toast.visible"
      @close="removeToast(index)"
    />
  </div>
</template>
