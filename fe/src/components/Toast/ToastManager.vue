<!--
================================================================================
 Component: ToastManager.vue
 Description:
        Manager for displaying multiple toast messages using a shared store.
        Renders all active toasts.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { useToastStore } from '@/stores/useToastStore';
import Toast from './Toast.vue';

const toastStore = useToastStore();

// Remove toast by index
const removeToast = (index) => {
  toastStore.removeToast(index);
};
</script>

<template>

  <div>
    <!-- Loop through all toasts in the store and render them -->
    <Toast
      v-for="(toast, index) in toastStore.toasts"
      :key="index"
      :message="toast.message"
      :type="toast.type"
      :visible="toast.visible"
      @close="removeToast(index)"
    />
  </div>
  
</template>
