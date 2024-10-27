<script setup>
import {ref, onMounted, computed, watch, nextTick } from 'vue';

const props = defineProps({
    number: {
        type: Number,
        
    }
});

const exampleInput = ref('');
const answerInput = ref('');
const focused = ref(false);

// Rendered previews for LaTeX
const renderedExample = computed(() => `\\(${exampleInput.value}\\)`);
const renderedAnswer = computed(() => `\\(${answerInput.value}\\)`);

// Function to render MathJax
function renderMathJax() {
    if (window.MathJax) {
        window.MathJax.typeset();
    }
}

// Watch for changes in input fields to render LaTeX
watch(exampleInput, async () => {
    await nextTick();
    renderMathJax();
});

watch(answerInput, async () => {
    await nextTick();
    renderMathJax();
});


const getData = () => {
    if(exampleInput.value !== "" && answerInput.value !== ""){
    return {
        example: exampleInput.value,
        answer: answerInput.value,
    };
    }else{
        return null;
    }
};


defineExpose({ getData });

onMounted(() => {
    renderMathJax();
});

</script>

<template>
    <div
      class="p-2 rounded-lg border-2 border-secondary"
      :class="{ 'ring-4 ring-main': focused }"
      @focusin="focused = true"
      @focusout="focused = false"
      tabindex="0"
    >
      <div class="flex justify-center items-center text-white bg-secondary rounded-full w-8 h-8">
        {{ number }}
      </div>
      <div class="flex justify-center p-2">
        <div class="flex flex-col mr-1">
          <h2 class="text-secondary font-bold">Zadání příkladu:</h2>
          <textarea
            v-model="exampleInput"
            placeholder="Zde vložte zadání příkladu"
            class="h-20 p-2 border border-gray-300 rounded mb-1"
          ></textarea>
          <input
            type="text"
            v-model="answerInput"
            placeholder="Zde vložte správnou odpověď"
            class="h-12 p-2 border border-gray-300 rounded"
          />
        </div>
  
        <div>
          <h2 class="text-secondary font-bold">Náhled:</h2>
          <div
            class="border border-gray-300 p-2 h-20 w-48 mb-1 text-md max-w-48"
            v-html="renderedExample"
          ></div>
          <div
            class="border border-gray-300 p-2 h-12 w-48"
            v-html="renderedAnswer" 
          ></div>
        </div>
      </div>
    </div>
</template>
