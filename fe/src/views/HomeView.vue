<script setup>
import Topics from '@/components/MainMenu/Topics.vue';
import { RouterLink, useRoute } from 'vue-router';


</script>

<template>

  <Topics></Topics>

  <div class="flex flex-col items-center justify-center mt-32">
    <RouterLink to="/tasks" class="cursor-pointer border-gray-800 border-2 rounded-lg shadow-lg max-w-md bg-white hover:bg-gray-200">
      <h2 class="flex justify-center text-2xl text-center font-bold text-gray-800 p-4">
          Sady příkladů
        </h2>
    </RouterLink>

    <RouterLink to="/skill-creator" class="cursor-pointer border-gray-800 border-2 rounded-lg shadow-lg max-w-md bg-white hover:bg-gray-200 mt-8">
      <h2 class="flex justify-center text-2xl text-center font-bold text-gray-800 p-4">
          Přidat dovednost
        </h2>
    </RouterLink>
    
  </div>
  


</template>