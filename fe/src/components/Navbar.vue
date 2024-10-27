<script setup>
import { RouterLink, useRoute } from 'vue-router';

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};
</script>

<template>
  <nav class="bg-primary shadow">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-9">
      <div class="flex h-20 items-center justify-between">
        <!-- Left: Brand/Logo -->
        <div class="flex items-center">
          <RouterLink to="/" class="text-4xl font-black tracking-wide text-white">DRILLOVAČKA</RouterLink>
        </div>

        <!-- Right: Navigation Links -->
        <div class="hidden md:flex space-x-8 items-center">
          <RouterLink to="/" class="text-2xl font-bold text-white">Příklady</RouterLink>
          <RouterLink to="/" class="text-2xl font-bold text-white">Přihlásit se</RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>


  