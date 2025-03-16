<script setup>
import { ref, computed, defineExpose } from 'vue';

const startTime = ref(null);
const timeElapsed = ref(0);
let intervalId = null; 

const startTimer = () => {
  startTime.value = performance.now(); 
  timeElapsed.value = 0; 

  intervalId = setInterval(() => {
    timeElapsed.value = performance.now() - startTime.value; // store time in milliseconds
  }, 100); 
};

const stopTimer = () => {
  if (intervalId !== null) {
    clearInterval(intervalId); 
    intervalId = null; 
  }
};

const getTime = () => {
    return timeElapsed.value; // returns time in milliseconds
}

defineExpose({
    startTimer,
    getTime
})

// Updated formattedTime to show in minutes:seconds format
const formattedTime = computed(() => {
  const minutes = Math.floor(timeElapsed.value / 60000); // 1 minute = 60,000 milliseconds
  const seconds = Math.floor((timeElapsed.value % 60000) / 1000); // Remaining seconds
  return `${minutes}:${seconds.toString().padStart(2, '0')}`; // Format as minutes:seconds
});
</script>

<template>
  <div class="p-4">
    <p v-if="timeElapsed !== null" class="text-2xl md:text-3xl font-semibold text-center">
      {{formattedTime}}
    </p>
  </div>
</template>
