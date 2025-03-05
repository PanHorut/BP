<script setup>
import { ref } from 'vue';

// Define the component props
const props = defineProps({
  number: {
    type: Number,
  },
  
});

const exampleInput = ref('');
const exampleId = ref('');  
const answerInput = ref(''); // Primary answer input (first one, not part of steps)
const stepInputs = ref([]); // Start with an empty array for steps
const focused = ref(false);

// Function to get data from inputs
const getData = () => {
  if (exampleInput.value !== "" && answerInput.value !== "") {

    return {
      example: exampleInput.value,
      example_id: exampleId.value ?? null,
      answer: answerInput.value,
      steps: stepInputs.value.map(step => step.value),
      input_type: "WORD"
    }; 
  } else {
    return null;
  }
};

const importExample = (example, id, answer, steps) => {
  exampleInput.value = example;
  exampleId.value = id;
  answerInput.value = answer;

  // depends if import is from Tasks overview or from JSON
  stepInputs.value = steps.map(step => {

    // from JSON
    if (typeof step === 'string') {
      return { value: step };

    // from task
    } else if (step.step_text) {
      return { value: step.step_text };
    }
  });  
}

const clearInput = () => {
  exampleInput.value = '';
  answerInput.value = '';
  stepInputs.value = [];
}


// Expose the getData method to parent components
defineExpose({ getData, importExample, clearInput });

// Add new step input when "+" button is clicked
const addStepInput = () => {
  stepInputs.value.push({ value: '' });
};

</script>

<template>
    <div
      class="p-4 rounded-lg border-2 border-secondary flex flex-col w-full"
      :class="{ 'ring-4 ring-main': focused }"
      @focusin="focused = true"
      @focusout="focused = false"
      tabindex="0"
    >
      <!-- Number Display -->
      <div class="flex justify-center items-center text-white bg-secondary rounded-full w-10 h-10 text-lg">
        {{ number }}
      </div>
  
      <!-- Example Input and Answer Input -->
      <div class="flex justify-center p-3">
        <div class="flex flex-col w-full">
          <h2 class="text-secondary font-bold mb-1">Zadání slovní úlohy:</h2>
          <textarea
            v-model="exampleInput"
            placeholder="Zde vložte zadání slovní úlohy"
            class="h-32 p-3 border border-gray-300 rounded w-full"
          ></textarea>
          
          <!-- Primary Answer Input -->
          <h2 class="text-secondary font-bold mt-3 mb-1">Správná odpověď:</h2>
          <input
            type="text"
            v-model="answerInput"
            placeholder="Zde vložte správnou odpověď"
            class="h-14 p-3 border border-gray-300 rounded w-full"
          />
  
          <!-- Dynamically Rendered Step Inputs -->
          <div v-if="stepInputs.length > 0" class="mt-3">
            <h2 class="text-secondary font-bold mb-1">Kroky řešení:</h2>
            <div v-for="(step, index) in stepInputs" :key="index" class="flex items-center mb-2">
              <textarea
                v-model="step.value"
                :placeholder="`Zde vložte ${index + 1}. krok řešení`"
                class="h-16 p-3 border border-gray-300 rounded w-full"
              ></textarea>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Add Step Button -->
      <div class="flex flex-col justify-center items-center mt-3">
        <div
          @click="addStepInput"
          class="self-center text-center bg-secondary text-white font-bold w-12 h-12 rounded-full text-2xl flex items-center justify-center cursor-pointer"
        >
          +
        </div>
        <p class="text-sm text-secondary font-medium mt-1">Přidat krok řešení</p>
      </div>
    </div>
  </template>
  

