<!--
================================================================================
 Component: ProfileView.vue
 Description:
        Displays practicing view for selected topics, handles logic for displaying examples
        and user answers evaluation results.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import Example from '@/components/Example.vue';
import ProgressBar from '@/components/Example/ProgressBar.vue';
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { getExamples } from '@/api/apiClient';
import correctIcon from '@/assets/img/correct.png';
import wrongIcon from '@/assets/img/wrong.png'
import correctSoundSrc from '@/assets/audio/correct.mp3';
import wrongSoundSrc from '@/assets/audio/wrong.mp3';
import Spinner from '@/components/Spinner.vue';
import Summary from '@/components/Example/Summary.vue';
import Survey from '@/components/Example/Survey.vue';
import { useRecorderStore } from '@/stores/useRecorderStore';
import { useLanguageStore } from '@/stores/useLanguageStore';
import {dictionary} from '@/utils/dictionary';

const examples = ref([]); 

// Instance of the <Example> component
const exampleComponent = ref(null); 

// Index of the current example 
const curr_index = ref(0); 

const topics = ref([]);
const isCorrect = ref(false);
const showIcon = ref(false);
const images = ref({});
const loading = ref(true);

// Example was skipped
const isSkipped = ref(false);     

// Count of mistakes made in current example
const mistakes = ref(0);

// Count of examples which user skipped
const skipped = ref(0);

// Count of examples where user made 0, 1, 2 or 3 mistakes 
const noMistakes = ref(0);
const oneMistake = ref(0);
const twoMistakes = ref(0);
const threeMistakes = ref(0);

// Bools to determine what will be displayed next
const showSummary = ref(false);
const showSurvey = ref(false);
const showAnswer = ref(false);

// Stores
const recorderStore = useRecorderStore();
const langStore = useLanguageStore();
const route = useRoute();

// SFX when user answers correctly or incorrectly
const correctSound = new Audio(correctSoundSrc);
const wrongSound = new Audio(wrongSoundSrc);

// Determine how many exampless user practiced in session
const storedExamplesCounted = sessionStorage.getItem("examplesCounted");
const examplesCounted = ref(storedExamplesCounted ? parseInt(storedExamplesCounted, 10) : 0);

// Preload correct and wrong answer icons
const preloadMedia = () => {
  const correct = new Image();
  const wrong = new Image();

  correct.src = correctIcon;
  wrong.src = wrongIcon;

  images.value.correct = correct;
  images.value.wrong = wrong;
};

// Depending on how many mistakes user made in example add one to the corresponding counter
const evaluateMistakes = () => {

  if(isSkipped.value){
    skipped.value++;
  }else if(mistakes.value === 0){
    noMistakes.value++;
  }else if(mistakes.value === 1){
    oneMistake.value++;
  }else if(mistakes.value === 2){
    twoMistakes.value++;
  }else if(mistakes.value === 3){
    threeMistakes.value++;
    mistakes.value = 0;
    isSkipped.value = false;
    return true;
  }

  mistakes.value = 0;
  isSkipped.value = false;
  return false;
};

// Determine what to display depending on users answer
const displayNext = async (data) => {
  
  if (curr_index.value >= 0 && curr_index.value < examples.value.length) {
    
    // User skipped the example
    if (data.skipped) {
      isSkipped.value = true;
    
    // User answered correctly
    } else if (data.isCorrect) {
      correctSound.play();
      displayIcon(true);
    
    // User answered incorrectly for 3 times
    } else if (!data.isCorrect && data.nextExample) {
      wrongSound.play();  
      displayIcon(false);
      mistakes.value++;
    
    // User answered incorrectly once or twice
    } else {
      wrongSound.play();
      displayIcon(false);
      mistakes.value++;
      exampleComponent.value.getStep(mistakes.value)
      return;
    }

    showAnswer.value = evaluateMistakes();

    // User made 3 mistakes in example - correct answer will be displayed
    if(showAnswer.value){
      exampleComponent.value.displayAnswer();

      setTimeout(() => {
        curr_index.value++;
        if (curr_index.value === examples.value.length) {
          recorderStore.stopRecording();  
          recorderStore.student_answer = '';
          showSummary.value = true;
        }
      }, 1500);
    
    // Display next example
    }else{
      curr_index.value++;
    }
    
    // Update counted examples
    examplesCounted.value++;
    sessionStorage.setItem("examplesCounted", examplesCounted.value.toString());

    // Show survey question every 10th example
    if(examplesCounted.value % 10 === 0 ){
      showSurvey.value = true;
    }
    
    await nextTick();

    // All examples were practiced
    if (curr_index.value === examples.value.length) {
      recorderStore.stopRecording();  
      recorderStore.student_answer = '';
      showSummary.value = true;
    }
    
  }else {
    console.error("index is out of bounds:", curr_index.value);
  }
};

// Fetch examples based on selected topics
const fetchExamples = async (topics) => {
  try {
    examples.value = await getExamples(topics);

  } catch (error) {
    console.error("Failed to fetch examples:", error);

  } finally {

    loading.value = false;
  }
};

// Display correct or incorrect icon
const displayIcon = async (correct) => {

  isCorrect.value = correct;
  await nextTick();

  const icon = correct
    ? images.value.correct.src
    : images.value.wrong.src;

  showIcon.value = true;

  setTimeout(() => {
    showIcon.value = false; 
  }, 400);
};

// Display summary after practice ended
const displaySummary = () => {
  recorderStore.stopRecording();
  recorderStore.student_answer = '';
  showSummary.value = true;
};

onMounted(() => {
  preloadMedia();

  if (route.query.topics) {
      topics.value = JSON.parse(route.query.topics);
      fetchExamples(topics.value);
  }
});

</script>

<template>
  
    <Spinner v-if="loading" class="pt-48"/>

    <!-- Fallback if no examples were fetched -->
    <div v-if="examples.length === 0 && !loading" class="flex flex-col justify-center items-center">
      <h1 class="text-xl md:text-3xl font-bold text-center pt-20 text-primary mb-8">Pro tuto kombinaci dovedností zatím neexistují příklady :(</h1>

      <RouterLink to="/"
                class="text-center text-xl md:text-3xl bg-secondary hover:bg-white text-white hover:text-secondary border-4 border-secondary rounded-xl font-semibold px-3 py-2 md:px-4 md:py-2 cursor-pointer transition">
                {{ dictionary[langStore.language].backtoMainMenu }}
      </RouterLink>
    </div>

    <!-- Progress bar --> 
    <div v-if="examples.length > curr_index && !showSummary && !showSurvey" class="flex-col items-center justify-center">
      <ProgressBar :totalExamples="examples.length" :finishedExamples="curr_index"></ProgressBar>
    </div>

    <div class="flex items-center justify-center">
      
      <!-- Example component -->
      <Example ref="exampleComponent" v-if="examples.length > curr_index && !showSummary && !showSurvey" :example="examples[curr_index]" :answer="examples[curr_index].answers[0].answer" @answerSent="displayNext" @skipped="displayNext" @finished="displaySummary" :key="curr_index"></Example>
      
      <!-- Correct or incorrect icon -->
      <img v-if="examples.length > curr_index"   :src="isCorrect ? images.correct.src : images.wrong.src" 
      class="w-48 h-48 absolute top-64 z-50" :class="showIcon ? '' : 'hidden'" >

      <!-- Practice summary-->
      <Summary v-if="showSummary" :skipped="skipped"  :noMistakes="noMistakes" :oneMistake="oneMistake" :twoMistakes="twoMistakes" :threeMistakes="threeMistakes" :topics="topics"></Summary>
      
      <!-- Survey question -->
      <Survey v-if="showSurvey && !showSummary" @hideSurvey="showSurvey = false" :topics="topics"></Survey>
    
    </div>

</template>
