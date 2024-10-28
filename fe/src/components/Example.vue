<script setup>
import { ref, onMounted, onUnmounted, defineEmits, computed, watch } from 'vue';

const userInput = ref('');
const emits = defineEmits(['answerSent']);
const renderedExample = computed(() => `\\(${props.example.example}\\)`);

const sendAnswer = () => {
  
  emits('answerSent', userInput.value); 
  userInput.value = '';
}

const props = defineProps({
  example: {
    type: Object,
  }
});

watch(
  () => props.example,
  () => {
    renderMathJax();
  },
  { immediate: true }
);

const handleNumDown = (event) => {
    
};

function renderMathJax() {
  if (window.MathJax) {
    window.MathJax.typesetPromise()
      .then(() => console.log("MathJax rendered in Example component"))
      .catch((err) => console.error("MathJax rendering error:", err));
  } else {
    console.error("MathJax not loaded.");
  }
}


// Keydown event handler for enter key
const handleEnter = (event) => {
  if (event.key === 'Enter') {
    sendAnswer();
    
  }
};

// Set up event listeners on mount
onMounted(() => {
  window.addEventListener('keydown', handleNumDown);
  window.addEventListener('keydown', handleEnter);
  renderMathJax();
});

// Clean up event listeners on unmount
onUnmounted(() => {
  window.removeEventListener('keydown', handleNumDown);
  window.removeEventListener('keydown', handleEnter);
});
</script>

<template>
  <div class="flex items-center justify-center mt-60">
    <div class="flex flex-col">
      <p class="text-8xl">
        {{ renderedExample }} =
        <input
          type="text"
          v-model="userInput"
          @keydown="handleKeydown"
          class="text-start w-96 text-8xl border-none self-end p-0"
          placeholder="?"
          autofocus
        />
      </p>
    </div>
  </div>
  <div class="flex justify-center">
    <div @click="sendAnswer" class="text-center text-4xl font-black text-blue-600 border-4 border-blue-600 p-5 rounded-3xl cursor-pointer">
      Mám hotovo!
    </div>
  </div>
</template>
