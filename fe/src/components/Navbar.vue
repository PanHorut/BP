<script setup>
import { RouterLink, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/useAuthStore';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

// Auth Store
const authStore = useAuthStore();
const router = useRouter();

// Determine Active Link
const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};

// Computed Property for Auth State
const isAuthenticated = computed(() => authStore.isAuthenticated);
</script>

<template>
  <nav class="bg-primary shadow">
    <div class=" px-2 sm:px-6 lg:px-9">
      <div class="flex h-20 items-center justify-between">
        <!-- Left: Brand/Logo -->
        <div class="flex items-center">
          <RouterLink to="/" class="text-4xl font-black tracking-wide text-white">
            DRILLOVAČKA
          </RouterLink>
        </div>

        <div class="flex items-center justify-end space-x-8 text-2xl font-semibold">
          <!-- If Not Logged In -->
          <template v-if="!isAuthenticated">
            <RouterLink to="/profile" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Přihlásit se</RouterLink>
          </template>

          <template v-else-if="authStore.role == 'admin'">
            <RouterLink to="/tasks" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Příklady</RouterLink>
            <RouterLink to="/skill-creator" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Dovednosti</RouterLink>

            <button @click="authStore.logout(router)" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Odhlásit se</button> 
          </template>

          <!-- If Logged In -->
          <template v-else>
            <RouterLink to="/profile" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Můj účet</RouterLink>
            <button @click="authStore.logout(router)" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Odhlásit se</button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>
