<!--
================================================================================
 Component: Example.vue
 Description:
        Displays interface for practicing example including input fields, timer
        and speech recorder, sends user answers to the server to be evaluated.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, onMounted, onUnmounted, defineEmits, defineExpose, computed, watch, nextTick } from 'vue';
import InlineInput from '@/components/Input Fields/InlineInput.vue';
import FractionInput from './Input Fields/FractionInput.vue';
import VariableInput from './Input Fields/VariableInput.vue';
import Timer from '@/components/Example/Timer.vue';
import SpeechRecorder from '@/components/Example/SpeechRecorder.vue';
import Answer from '@/components/Example/Answer.vue';
import Tips from '@/components/Example/Tips.vue';
import { createRecord, skipExample, deleteRecord, checkAnswer } from '@/api/apiClient';
import { useAuthStore } from '@/stores/useAuthStore';
import { useRecorderStore } from '@/stores/useRecorderStore';
import { useLanguageStore } from '@/stores/useLanguageStore';
import { dictionary } from '@/utils/dictionary';

const props = defineProps({
  example: {
    type: Object,
  },
  answer: {
    type: String,
  }
});

const emits = defineEmits(['answerSent', 'skipped', 'finished']);

// Rendered latex form of example text
const renderedExample = computed(() => `\\(${props.example.example}\\)`);

// Input values
const inlineInput = ref(null);
const fractionInput = ref(null);
const variableInput = ref(null);

// Component instances
const timer = ref(null);
const speechRecorder = ref(null);
const step = ref('');

// Stores
const authStore = useAuthStore();
const recorderStore = useRecorderStore();
const langStore = useLanguageStore();

// Record that user practiced example data
const student_id = authStore.id || 1;
const record_date = ref('');


let isWordProblem = ref(false);
const showAnswer = ref(false);

// Sends answer to be evaluated for inline answers and emits evaluation result
const checkInline = async (answer) => {

  const result = await checkAnswer(student_id, props.example.id, record_date.value, timer.value.getTime(), answer, "inline");
  emits('answerSent', { isCorrect: result.isCorrect, nextExample: result.continue_with_next });

  if (!result.isCorrect) {
    clearInput();
  }
};

// Sends answer to be evaluated for fraction answers and emits evaluation result
const checkFraction = async (numerator, denominator) => {

  const answer = [numerator, denominator];
  const result = await checkAnswer(student_id, props.example.id, record_date.value, timer.value.getTime(), answer, "fraction");
  emits('answerSent', { isCorrect: result.isCorrect, nextExample: result.continue_with_next });

  if (!result.isCorrect) {
    clearInput();
  }
}

// Sends answer to be evaluated for variable answers and emits evaluation result
const checkVariables = async (variables) => {

  const answers = variables.map(variable => variable.answer);
  const result = await checkAnswer(student_id, props.example.id, record_date.value, timer.value.getTime(), answers, "variable");
  emits('answerSent', { isCorrect: result.isCorrect, nextExample: result.continue_with_next });

  if (!result.isCorrect) {
    clearInput();
  }
}

// Record that user practiced example creation
const initRecord = async () => {
  const result = await createRecord(student_id, props.example.id);
  record_date.value = result.date;
  if (speechRecorder.value) {
    speechRecorder.value.updateExampleData(student_id, props.example.id, props.example.input_type, record_date.value);
  }
}

// Skip current example
const skip = () => {
  skipExample(student_id, props.example.id, record_date.value);
  emits('skipped', { skipped: true });
}

// Finish practicing
const finish = () => {
  deleteRecord(student_id, props.example.id, record_date.value);
  emits('finished');
}

// Watch changes in example text to re-render latex
watch(
  () => props.example,
  () => {
    renderMathJax();
    isWordProblem = props.example.input_type == 'WORD';
  },
  { immediate: true }
);

// Render latex form of example text
function renderMathJax() {
  if (window.MathJax) {
    window.MathJax.typesetPromise()
  }
}

// Handle Enter key and send answer
const handleEnter = (event) => {
  if (event.key === 'Enter' && !showAnswer.value) {
    getAnswer();
  }

};

// Get answer from currently used input field
const getAnswer = () => {

  if (inlineInput.value != null) {
    inlineInput.value.getAnswer();

  } else if (variableInput.value != null) {
    variableInput.value.getAnswer();

  } else if (fractionInput.value != null) {
    fractionInput.value.getAnswer();
  }
}

// Clear currently used input field
const clearInput = () => {

  if (inlineInput.value != null) {
    inlineInput.value.clearInput();

  } else if (variableInput.value != null) {
    variableInput.value.clearInput();

  } else if (fractionInput.value != null) {
    fractionInput.value.clearInput();
  }
}

// Set up event listeners to handle Enter key and render latex
onMounted(() => {
  initRecord()
  window.addEventListener('keydown', handleEnter);
  renderMathJax();
  timer.value.startTimer();

  recorderStore.setEmitFunction(emits);

});

// Clean up event listener for Enter key 
onUnmounted(() => {
  window.removeEventListener('keydown', handleEnter);
});

// Get example step text depending on number of mistakes
const getStep = (mistakes) => {
  if (props.example && props.example.steps) {
    step.value = props.example.steps[mistakes - 1]?.text ?? step.value;
  }
  return null;
};

// Display correct answer to user
const displayAnswer = () => {
  showAnswer.value = true;
  nextTick(() => {
    setTimeout(() => {

      showAnswer.value = false;
    }, 1500);
  });
}

defineExpose({ getStep, displayAnswer });
</script>

<template>

  <div class="w-full flex flex-col items-center justify-center">

    <div class="absolute top-20 md:top-24 md:right-4 md:left-auto md:w-auto w-full z-0">

      <!-- Timer and terminate practice button -->
      <div class="flex justify-between items-center md:block md:w-auto">

        <Timer ref="timer" class="md:mb-4" />

        <div @click="finish" class="text-center text-lg md:text-xl font-extrabold  mr-2 md:mr-0 text-white bg-red-600 
         border-4 border-red-700 p-2 md:p-3 rounded-2xl cursor-pointer transition 
         shadow-lg hover:bg-red-700 hover:border-red-700 hover:scale-105"
          :class="showAnswer ? 'pointer-events-none' : ''">
          {{ dictionary[langStore.language].quit.toUpperCase() }}
        </div>

      </div>

    </div>

    <div class="flex items-center justify-center mt-10 md:mt-20">
      <div class="flex flex-col">

        <div :class="[
          isWordProblem ? 'text-xl md:text-3xl flex flex-col items-center' : 'text-4xl md:text-7xl flex flex-col',
          props.example.input_type == 'FRAC' ? 'text-5xl' : 'text-4xl']">

          <!-- Latex example text or plain text for word problem -->
          <div class="flex items-center justify-center" :class="isWordProblem ? 'w-2/3 ' : 'w-full'">
            {{ isWordProblem ? example.example : renderedExample }}
          </div>

          <!-- Input components -->
          <div class="flex flex-col md:flex-row mt-10 items-center justify-between md:ml-80">

            <div class="flex justify-start items-center">

              <!-- Equal sign for inline and fraction examples -->
              <p v-if="props.example.input_type == 'INLINE' || props.example.input_type == 'FRAC'" class="mr-2">=</p>

              <VariableInput v-if="props.example.input_type == 'VAR'" ref="variableInput" :answer="props.answer"
                @answerSent="checkVariables">
              </VariableInput>

              <FractionInput v-else-if="props.example.input_type == 'FRAC'" ref="fractionInput"
                @answerSent="checkFraction">
              </FractionInput>

              <InlineInput v-else-if="props.example.input_type == 'INLINE'" ref="inlineInput" 
                @answerSent="checkInline">
              </InlineInput>

              <InlineInput v-else-if="props.example.input_type == 'WORD'" ref="inlineInput" 
                @answerSent="checkInline">
              </InlineInput>

            </div>

            <!-- Speech recorder to enter answers by voice -->
            <SpeechRecorder ref="speechRecorder" class="mt-6 md:ml-8 md:mt-0"
              :class="showAnswer ? 'pointer-events-none' : ''">
            </SpeechRecorder>

          </div>

          <!-- Example hint -->
          <div v-if="step" class="mt-8">
            <p class="text-4xl text-center text-gray-600">Nápověda: <span class="font-semibold text-black">{{ step
                }}</span></p>
          </div>

        </div>

      </div>

    </div>

    <div class="flex flex-col items-center justify-center w-full">
      <div class="flex items-center justify-around  w-full md:w-1/3 ">

        <!-- Placeholder used for centering -->
        <Tips class="invisible" />

        <!-- Button to send answer to be evaluated -->
        <div @click="getAnswer" class=" text-center text-4xl font-extrabold text-white bg-green-500 
             border-4 border-green-600 p-5 rounded-3xl cursor-pointer my-6 
             transition ease-in-out hover:bg-green-600 hover:scale-105 shadow-lg"
          :class="showAnswer ? 'pointer-events-none' : ''">
          {{ dictionary[langStore.language].done.toUpperCase() }}
        </div>

        <!-- Tips how to enter answers by voice -->
        <Tips :class="{
          'invisible': langStore.language === 'en',
          'pointer-events-none': showAnswer
        }" />
      </div>

      <!-- Skip example button -->
      <div @click="skip" class="text-center text-2xl font-extrabold text-gray-700 bg-gray-200 
           border-4 border-gray-500 px-8 py-2 rounded-2xl cursor-pointer
           transition ease-in-out hover:bg-gray-300 hover:border-gray-700 hover:scale-105 shadow-md"
        :class="showAnswer ? 'pointer-events-none' : ''">
        {{ dictionary[langStore.language].skip.toUpperCase() }}
      </div>

    </div>

  </div>

  <!-- Correct answer -->
  <Answer v-if="showAnswer" class="absolute top-96 md:top-auto right-auto z-50"
    :answer="props.example.answers[0].answer">
  </Answer>

</template>
