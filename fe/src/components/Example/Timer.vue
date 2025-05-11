<!--
================================================================================
 Component: Timer.vue
 Description:
        Displays elapsed time user practices current example.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, computed, defineExpose } from 'vue';

const startTime = ref(null);
const timeElapsed = ref(0);
let intervalId = null; 

// Start the timer
const startTimer = () => {
  startTime.value = performance.now(); 
  timeElapsed.value = 0; 

  intervalId = setInterval(() => {
    timeElapsed.value = performance.now() - startTime.value;
  }, 100); 
};

// Stop the timer
const stopTimer = () => {
  if (intervalId !== null) {
    clearInterval(intervalId); 
    intervalId = null; 
  }
};

// Get elapsed time
const getTime = () => {
    return timeElapsed.value;
}

// Format elapsed time to be displayed in minutes and seconds
const formattedTime = computed(() => {
  const minutes = Math.floor(timeElapsed.value / 60000); 
  const seconds = Math.floor((timeElapsed.value % 60000) / 1000);
  return `${minutes}:${seconds.toString().padStart(2, '0')}`; 
});

defineExpose({
    startTimer,
    getTime
})

</script>

<template>
  
  <div class="p-4">
    <p v-if="timeElapsed !== null" class="text-2xl md:text-3xl font-semibold text-center">
      {{formattedTime}}
    </p>
  </div>
</template>
