<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';

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

// Rendered previews for LaTeX
const renderedExample = computed(() => `\\(${exampleInput.value}\\)`);
const renderedAnswer = computed(() => `\\(${answerInput.value}\\)`); // Rendered answer
const renderedSteps = computed(() => stepInputs.value.map(step => `\\(${step.value}\\)`)); // Rendered steps

// Function to render MathJax
function renderMathJax() {
  if (window.MathJax) {
    window.MathJax.typeset();
  }
}

// Watch for changes in inputs to re-render LaTeX
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

// Function to get data from inputs
const getData = () => {
  if (exampleInput.value !== "" && answerInput.value !== "") {

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

    }else if(answerInput.value.includes('in')){

      return {
      example: exampleInput.value,
      example_id: exampleId.value ?? null,
      answer: answerInput.value,
      steps: stepInputs.value.map(step => step.value),
      input_type: "SET"
      };

    }else{
      
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

onMounted(() => {
  renderMathJax();
});

// Add new step input when "+" button is clicked
const addStepInput = () => {
  stepInputs.value.push({ value: '' });
};

</script>

<template>
  <div
    class="p-2 rounded-lg border-2 border-secondary flex flex-col"
    :class="{ 'ring-4 ring-main': focused }"
    @focusin="focused = true"
    @focusout="focused = false"
    tabindex="0"
  >
    <!-- Number Display -->
    <div class="flex justify-center items-center text-white bg-secondary rounded-full w-8 h-8">
      {{ number }}
    </div>

    <!-- Example Input and Answer Input -->
    <div class="flex justify-center p-2">
      <div class="flex flex-col mr-1">
        <h2 class="text-secondary font-bold">Zadání příkladu:</h2>
        <textarea
          v-model="exampleInput"
          placeholder="Zde vložte zadání příkladu"
          class="h-20 p-2 border border-gray-300 rounded mb-1"
        ></textarea>
        
        <!-- Primary Answer Input -->
        <input
          type="text"
          v-model="answerInput"
          placeholder="Zde vložte správnou odpověď"
          class="h-12 p-2 border border-gray-300 rounded mb-1"
        />

        <!-- Dynamically Rendered Step Inputs, only if steps exist -->
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

      <!-- Example and Answer Previews -->
      <div class="flex flex-col">
        <h2 class="text-secondary font-bold">Náhled:</h2>
        <!-- Rendered Example -->
        <div
        class="border border-gray-300 p-2 h-20 w-48 mb-1 text-md max-w-48 mjx-container"
        v-html="renderedExample"
        ></div>
        <!-- Rendered Answer -->
        <div
          class="border border-gray-300 p-2 h-12 w-48 mb-1 text-md max-w-48 mjx-container"
          v-html="renderedAnswer"
        ></div>

        <!-- Dynamically Rendered Step Previews, only if steps exist -->
        <div v-if="renderedSteps.length > 0" class="flex flex-col">
          <div v-for="(step, index) in renderedSteps" :key="index"
            class="border border-gray-300 p-2 h-12 w-48 mb-1 text-md mjx-container"
            v-html="step"
          ></div>
        </div>
      </div>
    </div>

    <!-- Add Step Button -->
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

<style scoped>
.mjx-container {
  display: inline-grid;
  overflow-wrap: break-word;
  overflow-x: auto;
  overflow-y: hidden;
}
</style>