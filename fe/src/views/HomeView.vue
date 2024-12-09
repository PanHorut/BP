<script setup>
import Topics from '@/components/MainMenu/Topics.vue';
import { RouterLink, useRoute } from 'vue-router';

import { ref, onMounted } from 'vue';

</script>

<template>

  <Topics></Topics>
  <div class="flex justify-center">
    <RouterLink to="/sandbox" class="border-4 border-black p-4 cursor-pointer text-2xl font-black rounded-lg">
      SANDBOX
    </RouterLink>
    
  </div>
  <p class="flex justify-center text-green-600 font-bold text-4xl mt-5">ONLINE</p>


</template>