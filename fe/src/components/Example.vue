<script setup>
import { ref, onMounted, onUnmounted, defineEmits } from 'vue';

const userInput = ref('');
const emits = defineEmits(['answerSent']);

const sendAnswer = () => {
  
  emits('answerSent', userInput.value); 
  userInput.value = '';
  
  
}
// Define props
const props = defineProps({
  example: {
    type: String,
    default: '',
  }
});

const handleNumDown = (event) => {
    const isNumericKey = /^[0-9]$/.test(event.key); // Check if the key pressed is a number
    const isBackspace = event.key === 'Backspace'; // Allow backspace

    // If it's not a number and not backspace, prevent the input
    if (!isNumericKey && !isBackspace) {
        event.preventDefault();
    }
};


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
        {{ example }} =
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
