<script setup>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { RouterView } from 'vue-router';
import ToastManager from '@/components/Toast/ToastManager.vue';
import { onMounted, onBeforeUnmount, watch } from 'vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { useRouter, useRoute } from 'vue-router';
import { useLanguageStore } from './stores/useLanguageStore';


const authStore = useAuthStore();
const langStore = useLanguageStore();
const router = useRouter();
const route = useRoute();


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

watch(
   () => langStore.language,
  () => {
    if (langStore.language === 'en') {
      document.title = 'Drillapp';
    } else {
      document.title = 'Drillovačka';
    }
  },
  { immediate: true }
);

</script>

<template>
  <Navbar />
  <ToastManager />

  <div class="bg-white min-h-screen">
    <RouterView />
  </div>

  <Footer />
  

</template>