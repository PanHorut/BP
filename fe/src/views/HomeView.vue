<script setup>
import Topics from '@/components/Topics.vue';
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

</template>