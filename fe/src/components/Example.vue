<script setup>
import { ref, onMounted, onUnmounted, defineEmits, defineExpose, computed, watch, nextTick } from 'vue';
import InlineInput from '@/components/Input Fields/InlineInput.vue';
import FractionInput from './Input Fields/FractionInput.vue';
import VariableInput from './Input Fields/VariableInput.vue';
import SetInput from './Input Fields/SetInput.vue';
import Timer from '@/components/Example/Timer.vue';
import SpeechRecorder from '@/components/Example/SpeechRecorder.vue';
import { updateRecord, createRecord, skipExample, deleteRecord, checkAnswer } from '@/api/apiClient';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/useAuthStore';
import { useRecorderStore } from '@/stores/useRecorderStore';

const props = defineProps({
  example: {
    type: Object,
  },
  answer:{
    type: String,
  }
});

const emits = defineEmits(['answerSent', 'skipped', 'finished']);
const renderedExample = computed(() => `\\(${props.example.example}\\)`);
const inlineInput = ref(null);
const fractionInput = ref(null);
const setInput = ref(null);
const variableInput = ref(null);
const timer = ref(null);
const record_date = ref('');
const router = useRouter();
const authStore = useAuthStore(); 
const student_id = authStore.id || 1;
const speechRecorder = ref(null);
const recorderStore = useRecorderStore(); 

let isWordProblem = ref(false);

const checkInline = async (answer) => {

  
  const result = await checkAnswer(student_id, props.example.id, record_date.value, timer.value.getTime(), answer, "inline"); 
  emits('answerSent', {isCorrect: result.isCorrect, nextExample: result.continue_with_next});

  if(!result.isCorrect){
    clearInput();
  }

};

const checkFraction = async (numerator, denominator) => {

  const answer = [numerator, denominator];
  const result = await checkAnswer(student_id, props.example.id, record_date.value, timer.value.getTime(), answer, "fraction");
  emits('answerSent', {isCorrect: result.isCorrect, nextExample: result.continue_with_next}); 

  if(!result.isCorrect){
    clearInput();
  }

}

const checkVariables = async (variables) => {

  const answers = variables.map(variable => variable.answer);
  const result = await checkAnswer(student_id, props.example.id, record_date.value, timer.value.getTime(), answers, "variable");
  emits('answerSent', {isCorrect: result.isCorrect, nextExample: result.continue_with_next}); 

  if(!result.isCorrect){
    clearInput();
  }
}

const checkSet = async (variables) => {
  for (const variable of variables) {

    if(variable.answer == variable.correctAnswer){
      continue;

    }else{
      // false answer
      const result = await updateRecord(student_id, props.example.id, false, timer.value.getTime(), record_date.value);
      emits('answerSent', {isCorrect: false, nextExample: result.next_example});
      clearInput();

      return;
    }
  }
  const result = await updateRecord(student_id, props.example.id, true, timer.value.getTime(), record_date.value);
  emits('answerSent', {isCorrect: true, nextExample: true});
}

const initRecord = async () => {
  const result = await createRecord(student_id , props.example.id);
  record_date.value = result.date;
  if (speechRecorder.value) {
      speechRecorder.value.updateExampleData(student_id, props.example.id, props.example.input_type, record_date.value);
  }
  
}

const skip = async () => {
  const result = await skipExample(student_id , props.example.id, record_date.value);
  emits('skipped', {skipped: true});

}

const finish = async () => {
  const result = await deleteRecord(student_id , props.example.id, record_date.value);
  emits('finished');

}

watch(
  () => props.example,
  () => {
    renderMathJax();
    isWordProblem = props.example.input_type == 'WORD';
  },
  { immediate: true }
);



function renderMathJax() {
  if (window.MathJax) {
    window.MathJax.typesetPromise()
      
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

const clearInput = () => {

  if(inlineInput.value != null){
    inlineInput.value.clearInput();

  } else if(variableInput.value != null){
    variableInput.value.clearInput();

  }else if(setInput.value != null){
    setInput.value.clearInput();

  }else if(fractionInput.value != null){
    fractionInput.value.clearInput();
  }
}

// Set up event listeners on mount
onMounted(() => {
  initRecord()
  window.addEventListener('keydown', handleEnter);
  renderMathJax();
  timer.value.startTimer();

  recorderStore.setEmitFunction(emits);

});

// Clean up event listeners on unmount
onUnmounted(() => {
  window.removeEventListener('keydown', handleEnter);
});

const step = ref('');

const getStep = (mistakes) => {
  if (props.example && props.example.steps) {
    step.value = props.example.steps[mistakes - 1]?.text ?? step.value;
  }
  return null;
};

defineExpose({getStep});

</script>

<template>
  <div class="w-full flex flex-col items-center justify-center">
    <div class="absolute right-4 top-24">
      <Timer ref="timer" ></Timer>
      <div @click="finish" class="text-center text-xl font-bold text-white hover:text-red-600 bg-red-600 hover:bg-white border-4 border-red-600 p-2 rounded-2xl cursor-pointer">
        UKONČIT
    </div>
    </div>
  <div class="flex items-center justify-center mt-20">
    
    <div class="flex flex-col">
      <div :class="isWordProblem ? 'text-3xl flex flex-col items-center' : 'text-8xl'">
       
          <div class="flex items-center" :class="isWordProblem ? 'w-2/3 ' : 'w-32'">
            {{isWordProblem ? example.example : renderedExample }}
          </div>
          
        <div class="flex mt-10 items-center">
        <p v-if="props.example.input_type == 'INLINE' || props.example.input_type == 'FRAC'" class="mr-2">=</p>
          <VariableInput v-if="props.example.input_type == 'VAR'" ref="variableInput" :answer="props.answer" @answerSent="checkVariables"></VariableInput>
          <FractionInput v-else-if="props.example.input_type == 'FRAC'" ref="fractionInput" @answerSent="checkFraction"></FractionInput>
          <SetInput v-else-if="props.example.input_type == 'SET'" ref="setInput" :answer="props.answer" @answerSent="checkSet"></SetInput>      
          <InlineInput v-else-if="props.example.input_type == 'INLINE'" ref="inlineInput" @answerSent="checkInline"></InlineInput>
          <InlineInput v-else-if="props.example.input_type == 'WORD'" ref="inlineInput" @answerSent="checkInline"></InlineInput>
          <SpeechRecorder ref="speechRecorder" class="ml-8"></SpeechRecorder>

      </div>
      <div v-if="step" class="mt-8">
        <p class="text-4xl text-center text-gray-600">Nápověda: <span class="font-semibold text-black">{{ step }}</span></p>
      </div>
    </div>
    </div>
  </div>
  <div class="flex flex-col items-center justify-center">
    <div @click="getAnswer" class="text-center text-4xl font-black text-blue-600 border-4 border-blue-600 p-5 rounded-3xl cursor-pointer my-10">
      Mám hotovo!
    </div>

    <div @click="skip" class="text-center text-2xl font-black text-gray-600 border-4 border-gray-600 px-8 py-2 rounded-3xl cursor-pointer mt-4">
      NEVÍM
    </div>


  </div>
</div>
</template>
