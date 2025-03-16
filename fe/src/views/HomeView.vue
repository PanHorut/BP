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
      Vítejte na hlavní stránce
    </p>

    <div class="flex flex-col items-center justify-center gap-8 pt-16">
      <RouterLink to="/tasks" class="w-96 cursor-pointer border border-gray-300 rounded-lg shadow-lg max-w-md bg-white 
           transition transform  hover:shadow-xl 
           hover:bg-secondary hover:border-secondary flex items-center justify-center text-3xl text-center font-bold text-primary p-4 
              duration-300 ease-in-out hover:text-white">
        Příklady
      </RouterLink>
      <RouterLink to="/skill-creator" class="w-96 cursor-pointer border border-gray-300 rounded-lg shadow-lg max-w-md bg-white 
           transition transform  hover:shadow-xl 
           hover:bg-secondary hover:border-secondary flex items-center justify-center text-3xl text-center font-bold text-primary p-4 
              duration-300 ease-in-out hover:text-white"> Dovednosti
      </RouterLink>
    </div>
  </div>
</template>
