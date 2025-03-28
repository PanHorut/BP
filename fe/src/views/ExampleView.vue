<script setup>
import Example from '@/components/Example.vue';
import ProgressBar from '@/components/Example/ProgressBar.vue';
import SpecialCharsBar from '@/components/Example/SpecialCharsBar.vue';
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

const examples = ref([]); 
const exampleComponent = ref(null);  
const curr_index = ref(0); 
const route = useRoute();
const topics = ref([]);

const isCorrect = ref(false);
const showIcon = ref(false);

const images = ref({});

const loading = ref(true);

const isSkipped = ref(false);     

const mistakes = ref(0);

const skipped = ref(0);
const noMistakes = ref(0);
const oneMistake = ref(0);
const twoMistakes = ref(0);
const threeMistakes = ref(0);

const showSummary = ref(false);

const showSurvey = ref(false);

const recorderStore = useRecorderStore();

const correctSound = new Audio(correctSoundSrc);
const wrongSound = new Audio(wrongSoundSrc);

const preloadMedia = () => {
  const correct = new Image();
  const wrong = new Image();

  correct.src = correctIcon;
  wrong.src = wrongIcon;

  images.value.correct = correct;
  images.value.wrong = wrong;
};

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
  }

  mistakes.value = 0;
  isSkipped.value = false;
};


const displayNext = async (data) => {
  

  if (curr_index.value >= 0 && curr_index.value < examples.value.length) {
    
    if (data.skipped) {
      isSkipped.value = true;
    } 
    else if (data.isCorrect) {
      correctSound.play();
      displayIcon(true);
    } 
    else if (!data.isCorrect && data.nextExample) {
      wrongSound.play();  
      displayIcon(false);
      mistakes.value++;
    } 
    else {
      wrongSound.play();
      displayIcon(false);
      mistakes.value++;
      exampleComponent.value.getStep(mistakes.value)
      return;
    }
    evaluateMistakes();
    
    curr_index.value++;

    // show survey every 10th example
    if(curr_index.value % 10 === 0 ){
      showSurvey.value = true;
    }
    

    await nextTick();

    if (curr_index.value === examples.value.length) {
      recorderStore.stopRecording();  
      recorderStore.student_answer = '';
      showSummary.value = true;
    }
    
  }else {
    console.error("index is out of bounds:", curr_index.value);
  }
};

const fetchExamples = async (topics) => {
  
  try {
    examples.value = await getExamples(topics);
  } catch (error) {
    console.error("Failed to fetch examples:", error);
  } finally {
    loading.value = false;
  }
 
};

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
    <!--<SpecialCharsBar v-if="examples.length > curr_index && !showSummary"></SpecialCharsBar>-->
    <div v-if="examples.length > curr_index && !showSummary && !showSurvey" class="flex-col items-center justify-center">
      <ProgressBar :totalExamples="examples.length" :finishedExamples="curr_index"></ProgressBar>
      <Spinner v-if="loading" class="mt-48"/>
    </div>
    <div class="flex items-center justify-center">
             
      <Example ref="exampleComponent" v-if="examples.length > curr_index && !showSummary && !showSurvey" :example="examples[curr_index]" :answer="examples[curr_index].answers[0].answer" @answerSent="displayNext" @skipped="displayNext" @finished="displaySummary" :key="curr_index"></Example>
      <img v-if="examples.length > curr_index"   :src="isCorrect ? images.correct.src : images.wrong.src" 
      class="w-48 h-48 absolute top-64 z-50" :class="showIcon ? '' : 'hidden'" >

      
      <Summary v-if="showSummary" :skipped="skipped"  :noMistakes="noMistakes" :oneMistake="oneMistake" :twoMistakes="twoMistakes" :threeMistakes="threeMistakes"></Summary>
      <Survey v-if="showSurvey && !showSummary" @hideSurvey="showSurvey = false"></Survey>
    </div>

    
</template>
