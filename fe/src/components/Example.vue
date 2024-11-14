<script setup>
import { ref, onMounted, onUnmounted, defineEmits, computed, watch } from 'vue';
import InlineInput from '@/components/Input Fields/InlineInput.vue';
import FractionInput from './Input Fields/FractionInput.vue';
import VariableInput from './Input Fields/VariableInput.vue';
import SetInput from './Input Fields/SetInput.vue';



const props = defineProps({
  example: {
    type: Object,
  },
  answer:{
    type: String,
  }
});

const emits = defineEmits(['answerSent']);
const renderedExample = computed(() => `\\(${props.example.example}\\)`);
const inlineInput = ref(null);
const fractionInput = ref(null);
const setInput = ref(null);
const variableInput = ref(null);

const checkInline = (answer) => {

  if(props.answer == answer){
    emits('answerSent', true);
    console.log("CORRECT");

  }else{
    emits('answerSent', false);
    console.log("FALSE");
  }
  
  
};

const checkFraction = (numerator, denominator) => {
  const answer = extractFraction(props.answer);

  if(numerator == answer.numerator && denominator == answer.denominator){
    emits('answerSent', true);
    console.log("CORRECT");

  }else{
    emits('answerSent', false);
    console.log("FALSE");
  }
 
}

const checkVariables = (variables) => {
  
  for (const variable of variables) {

    if(variable.answer == variable.correctAnswer){
      continue;

    }else{
      emits('answerSent', false);
      console.log("FALSE");
      return;
    }
  }
  emits('answerSent', true);
  console.log("CORRECT"); 
}

const checkSet = (variables) => {
  for (const variable of variables) {

    if(variable.answer == variable.correctAnswer){
      continue;

    }else{
      emits('answerSent', false);
      console.log("FALSE");
      return;
    }
  }
  emits('answerSent', true);
  console.log("CORRECT"); 
}

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

const handleEnter = (event) => {
  if (event.key === 'Enter') {
    getAnswer();
  }
};

const getAnswer = () =>{
  
    if(inlineInput.value != null){
      inlineInput.value.getAnswer();

    } else if(variableInput.value != null){
      variableInput.value.getAnswer();

    }else if(setInput.value != null){
      setInput.value.getAnswer();

    }else if(fractionInput.value != null){
      fractionInput.value.getAnswer();
    }
    
  
}

function extractFraction(fraction) {
  const regex = /\\frac\{([^\}]+)\}\{([^\}]+)\}/; // Matches \frac{numerator}{denominator}
  const match = fraction.match(regex);

  if (match) {
    const numerator = match[1]; // Captures the numerator
    const denominator = match[2]; // Captures the denominator
    return { numerator, denominator };
  } else {
    console.error('Invalid fraction format');
    return null;
  }
}

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
  <div class="flex flex-col items-center justify-center">
  <div class="flex items-center justify-center mt-40">
    <div class="flex flex-col">
      <div class="text-8xl">
        <div class="flex w-32 items-center">
          {{ renderedExample }}
        </div>
        <div class="flex mt-10 items-center">
        <p v-if="props.example.input_type == 'INLINE' || props.example.input_type == 'FRAC'" class="mr-2">=</p>
          <VariableInput v-if="props.example.input_type == 'VAR'" ref="variableInput" :answer="props.answer" @answerSent="checkVariables"></VariableInput>
          <FractionInput v-else-if="props.example.input_type == 'FRAC'" ref="fractionInput" @answerSent="checkFraction"></FractionInput>
          <SetInput v-else-if="props.example.input_type == 'SET'" ref="setInput" :answer="props.answer" @answerSent="checkSet"></SetInput>      
          <InlineInput v-else-if="props.example.input_type == 'INLINE'" ref="inlineInput" @answerSent="checkInline"></InlineInput>
      </div>
    </div>
    </div>
  </div>
  <div class="flex justify-center">
    <div @click="getAnswer" class="text-center text-4xl font-black text-blue-600 border-4 border-blue-600 p-5 rounded-3xl cursor-pointer my-10">
      Mám hotovo!
    </div>
  </div>
</div>
</template>
