<script setup>
import Topics from '@/components/MainMenu/Topics.vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

// Auth Store
const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);

const router = useRouter();
</script>

<template>
  <Topics v-if="authStore.role != 'admin'"></Topics>
  <div v-else>
    <p class="text-4xl text-primary flex justify-center font-bold pt-16">
      Vítejte na hlavní stránce DRILLOVAČKA
    </p>
    
    <div class="flex flex-col items-center justify-center gap-8 pt-16">
      <RouterLink 
        to="/tasks" 
        class="w-96 py-3 bg-primary text-white text-2xl font-medium border-2 border-primary rounded-lg shadow-md hover:bg-white hover:text-primary hover:border-primary transition-all text-center flex items-center justify-center">
        Vytvořit příklady
      </RouterLink>
      <RouterLink 
        to="/skill-creator" 
        class="w-96 py-3 bg-primary text-white text-2xl font-medium border-2 border-primary rounded-lg shadow-md hover:bg-white hover:text-primary hover:border-primary transition-all text-center flex items-center justify-center">
        Vytvořit novou dovednost
      </RouterLink>
    </div>
  </div>
</template>

