<script setup>
import { ref, defineProps, computed } from "vue";

const props = defineProps({
  finishedExamples: {
    type: Number,
    required: true
  },
  totalExamples: {
    type: Number,
    required: true
  }
});

const progress = computed(() => {
  return props.totalExamples > 0 ? (props.finishedExamples / props.totalExamples) * 100 : 0;
});
</script>

<template>
    <div class="w-full max-w-md mx-auto mt-10">
      <!-- Progress Bar Container -->
      <div class="bg-gray-200 rounded-full h-6">
        <div
          class="bg-secondary h-6 rounded-full"
          :style="{ width: progress + '%' }"
        ></div>
      </div>
  
      <!-- Progress Label -->
      <div class="flex justify-center text-3xl font-semibold mt-2">
        
        <span>{{ finishedExamples }} / {{ totalExamples }}</span>
        
      </div>
    </div>
  </template>
  

  

  