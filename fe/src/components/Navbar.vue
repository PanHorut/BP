<script setup>
import { RouterLink, useRoute } from 'vue-router';

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};
</script>

<template>
  <nav class="bg-primary shadow">
    <div class="max-w-7xl px-2 sm:px-6 lg:px-9">
      <div class="flex h-20 items-center justify-between">
        <!-- Left: Brand/Logo -->
        <div class="flex items-center">
          <RouterLink to="/" class="text-4xl font-black tracking-wide text-white">DRILLOVAČKA</RouterLink>
        </div>

        <div>
          
        </div>
      </div>
    </div>
  </nav>
</template>


  