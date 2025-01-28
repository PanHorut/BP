<script setup>
import { ref, computed, defineExpose } from 'vue';

const startTime = ref(null);
const timeElapsed = ref(0);
let intervalId = null; 


const startTimer = () => {
  startTime.value = performance.now(); 
  timeElapsed.value = 0; 

  intervalId = setInterval(() => {
    timeElapsed.value = Math.floor((performance.now() - startTime.value) / 1000);
  }, 100); 
};

const stopTimer = () => {
  if (intervalId !== null) {
    clearInterval(intervalId); 
    intervalId = null; 
  }
};

const getTime = () =>{
    return timeElapsed.value;
}

defineExpose({
    startTimer,
    getTime
})

const formattedTime = computed(() => {
  const minutes = Math.floor(timeElapsed.value / 60);
  const seconds = timeElapsed.value % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
});
</script>

<template>
  <div class="p-4">

    <p v-if="timeElapsed !== null" class="mt-4 text-3xl font-semibold text-center">
      {{formattedTime}}
    </p>
  </div>
</template>