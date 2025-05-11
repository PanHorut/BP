<!--
================================================================================
 Component: ExampleCreator.vue
 Description:
        Allows admin to create a new example with steps and answer and also provide preview of its latex form.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';

const props = defineProps({
  number: {
    type: Number,
  },
  
});
const exampleId = ref('');  
const focused = ref(false);

// Input fields
const exampleInput = ref('');
const answerInput = ref(''); 
const stepInputs = ref([]);

// Rendered previews of input fields
const renderedExample = computed(() => `\\(${exampleInput.value}\\)`);
const renderedAnswer = computed(() => `\\(${answerInput.value}\\)`); 
const renderedSteps = computed(() => stepInputs.value.map(step => `\\(${step.value}\\)`)); 

// Add new step input
const addStepInput = () => {
  stepInputs.value.push({ value: '' });
};

// Render latex 
function renderMathJax() {
  if (window.MathJax) {
    window.MathJax.typeset();
  }
}

// Watch for changes in inputs to re-render latex
watch(exampleInput, async () => {
  await nextTick();
  renderMathJax();
});

watch(answerInput, async () => {
  await nextTick();
  renderMathJax();
});

watch(stepInputs, async () => {
  await nextTick();
  renderMathJax();
}, { deep: true });

// Get values from input fields
const getData = () => {
  if (exampleInput.value !== "" && answerInput.value !== "") {

    // Determine type of example based on answer format 
    if(answerInput.value.includes('=')){

      return {
      example: exampleInput.value,
      example_id: exampleId.value ?? null,
      answer: answerInput.value,
      steps: stepInputs.value.map(step => step.value),
      input_type: "VAR"
      };
      
    }else if(answerInput.value.includes('frac')){

      return {
      example: exampleInput.value,
      example_id: exampleId.value ?? null,
      answer: answerInput.value,
      steps: stepInputs.value.map(step => step.value),
      input_type: "FRAC"
      };

    } else{
      
      return {
      example: exampleInput.value,
      example_id: exampleId.value ?? null,
      answer: answerInput.value,
      steps: stepInputs.value.map(step => step.value),
      input_type: "INLINE"
      };

    }
  } else {
    return null;
  }
};

// Import example into input fields
const importExample = (example, id, answer, steps) => {
  exampleInput.value = example;
  exampleId.value = id;
  answerInput.value = answer;

  stepInputs.value = steps.map(step => {

    // from JSON file
    if (typeof step === 'string') {
      return { value: step };

    // from Task list (via Edit button)
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

onMounted(() => {
  renderMathJax();
});
</script>

<template>
  <div
    class="p-2 rounded-lg border-2 border-secondary flex flex-col"
    :class="{ 'ring-4 ring-main': focused }"
    @focusin="focused = true"
    @focusout="focused = false"
    tabindex="0"
  >
    <!-- Example number -->
    <div class="flex justify-center items-center text-white bg-secondary rounded-full w-8 h-8">
      {{ number }}
    </div>

    <!-- Example inputs -->
    <div class="flex justify-center p-2">
      <div class="flex flex-col mr-1">

        <h2 class="text-secondary font-bold">Zadání příkladu:</h2>

        <!-- Example text input field -->
        <textarea
          v-model="exampleInput"
          placeholder="Zde vložte zadání příkladu"
          class="h-20 p-2 border border-gray-300 rounded mb-1"
        ></textarea>

        <!-- Answer input field -->
        <input
          type="text"
          v-model="answerInput"
          placeholder="Zde vložte správnou odpověď"
          class="h-12 p-2 border border-gray-300 rounded mb-1"
        />

        <!-- Step input fields -->
        <div v-if="stepInputs.length > 0">
          <div v-for="(step, index) in stepInputs" :key="index" class="flex items-center mb-1">
            <textarea
              v-model="step.value"
              :placeholder="`Zde vložte ${ index+1 }. krok řešení`"
              class="h-12 p-2 border border-gray-300 rounded"
            ></textarea>
          </div>
        </div>

      </div>

      <!-- Example previews -->
      <div class="flex flex-col">

        <h2 class="text-secondary font-bold">Náhled:</h2>

        <!-- Rendered example -->
        <div
        class="border border-gray-300 p-2 h-20 w-48 mb-1 text-md max-w-48 mjx-container"
        v-html="renderedExample"
        ></div>

        <!-- Rendered answer -->
        <div
          class="border border-gray-300 p-2 h-12 w-48 mb-1 text-md max-w-48 mjx-container"
          v-html="renderedAnswer"
        ></div>

        <!-- Rendered steps -->
        <div v-if="renderedSteps.length > 0" class="flex flex-col">
          <div v-for="(step, index) in renderedSteps" :key="index"
            class="border border-gray-300 p-2 h-12 w-48 mb-1 text-md mjx-container"
            v-html="step"
          ></div>
        </div>

      </div>
    </div>

    <!-- Add step -->
    <div class="flex flex-col justify-center items-center">
      <div
        @click="addStepInput"
        class="self-center text-center bg-secondary text-white font-bold w-10 h-10 rounded-full text-xl flex items-center justify-center cursor-pointer"
      >
        +
      </div>
      <p class="text-sm text-secondary font-medium">Přidat krok řešení</p>
    </div>
  </div>
  
</template>

<!-- Style for latex preview -->
<style scoped>
.mjx-container {
  display: inline-grid;
  overflow-wrap: break-word;
  overflow-x: auto;
  overflow-y: hidden;
}
</style>