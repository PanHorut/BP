<!--
================================================================================
 Component: WordProblemCreator.vue
 Description:
        Allows admin to create new example with steps and answer in form of word problem.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref } from 'vue';

const props = defineProps({
  number: {
    type: Number,
  },
  
});

// Input fields
const exampleInput = ref(''); 
const answerInput = ref(''); 
const stepInputs = ref([]);

const exampleId = ref(''); 
const focused = ref(false);

// Add new step input
const addStepInput = () => {
  stepInputs.value.push({ value: '' });
};

// Get values from input fields
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

// Import example into input fields
const importExample = (example, id, answer, steps) => {
  exampleInput.value = example;
  exampleId.value = id;
  answerInput.value = answer;

  // Depends if import is from Tasks list or from JSON
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

// Clear input fields
const clearInput = () => {
  exampleInput.value = '';
  answerInput.value = '';
  stepInputs.value = [];
}

defineExpose({ getData, importExample, clearInput });
</script>

<template>
    <div
      class="p-4 rounded-lg border-2 border-secondary flex flex-col w-full"
      :class="{ 'ring-4 ring-main': focused }"
      @focusin="focused = true"
      @focusout="focused = false"
      tabindex="0"
    >
      <!-- Example number -->
      <div class="flex justify-center items-center text-white bg-secondary rounded-full w-10 h-10 text-lg">
        {{ number }}
      </div>
  
      <!-- Example inputs -->
      <div class="flex justify-center p-3">
        <div class="flex flex-col w-full">
          <h2 class="text-secondary font-bold mb-1">Zadání slovní úlohy:</h2>

          <!-- Example text input field -->
          <textarea
            v-model="exampleInput"
            placeholder="Zde vložte zadání slovní úlohy"
            class="h-32 p-3 border border-gray-300 rounded w-full"
          ></textarea>
          
          
          <h2 class="text-secondary font-bold mt-3 mb-1">Správná odpověď:</h2>

          <!-- Answer input field -->
          <input
            type="text"
            v-model="answerInput"
            placeholder="Zde vložte správnou odpověď"
            class="h-14 p-3 border border-gray-300 rounded w-full"
          />
  
          <!-- Steps input fields -->
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
  
      <!-- Add step -->
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