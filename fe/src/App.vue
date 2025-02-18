<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
import ToastManager from '@/components/Toast/ToastManager.vue';
import { onMounted, onBeforeUnmount } from 'vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const resetInactivity = () => {
  if (authStore.isAuthenticated) {
    authStore.resetInactivityTimer(router);
  }
};

onMounted(() => {
  window.addEventListener('mousemove', resetInactivity);
  window.addEventListener('keydown', resetInactivity);
});

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', resetInactivity);
  window.removeEventListener('keydown', resetInactivity);
});

</script>

<template>
  <Navbar />
  <ToastManager />

  <div class="bg-white min-h-screen">
    <RouterView />
  </div>

</template>