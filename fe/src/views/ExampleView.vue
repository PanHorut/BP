<script setup>
import Example from '@/components/Example.vue';
import ProgressBar from '@/components/Example/ProgressBar.vue';
import SpecialCharsBar from '@/components/Example/SpecialCharsBar.vue';
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { getExamples } from '@/api/apiClient';
import correctIcon from '@/assets/img/correct.png';
import wrongIcon from '@/assets/img/wrong.png'
import Spinner from '@/components/Spinner.vue';
import Summary from '@/components/Example/Summary.vue';

const examples = ref([]); 
const curr_index = ref(0); 
const route = useRoute();
const topics = ref([]);

const isCorrect = ref(false);
const showIcon = ref(false);

const images = ref({});

const loading = ref(true);

const mistakes = ref(0);
const skipped = ref(0);
const total = ref(0); 

const showSummary = ref(false);

const preloadImages = () => {
  const correct = new Image();
  const wrong = new Image();

  correct.src = correctIcon;
  wrong.src = wrongIcon;

  images.value.correct = correct;
  images.value.wrong = wrong;
};


const displayNext = async (data) => {
  

  if (curr_index.value >= 0 && curr_index.value < examples.value.length) {
    
    if (data.skipped) {
      skipped.value++;
    } 
    else if (data.isCorrect) {
      displayIcon(true);
    } 
    else if (!data.isCorrect && data.nextExample) {
      displayIcon(false);
      mistakes.value++;
    } 
    else {
      mistakes.value++;
      displayIcon(false);
      return;
    }

    curr_index.value++;
    await nextTick();

    if (curr_index.value === examples.value.length) {
      total.value = examples.value.length - skipped.value;  
      showSummary.value = true;
    }
    
  }else {
    console.error("index is out of bounds:", curr_index.value);
  }
};

const fetchExamples = async (topics) => {
  
  try {
    examples.value = await getExamples(topics);
    total.value = examples.value.length;
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
  total.value = curr_index.value-1;
  showSummary.value = true;
};


onMounted(() => {
  preloadImages();

  if (route.query.topics) {
      topics.value = JSON.parse(route.query.topics);
      fetchExamples(topics.value);
  }
});
</script>

<template>
    <SpecialCharsBar v-if="examples.length > curr_index && !showSummary"></SpecialCharsBar>
    <div v-if="examples.length > curr_index && !showSummary" class="flex-col items-center justify-center">
      <ProgressBar :totalExamples="examples.length" :finishedExamples="curr_index"></ProgressBar>
      <Spinner v-if="loading" class="mt-48"/>
    </div>
    <div class="flex items-center justify-center">
      
      
      <Example v-if="examples.length > curr_index && !showSummary" :example="examples[curr_index]" :answer="examples[curr_index].answers[0].answer" @answerSent="displayNext" @skipped="displayNext" @finished="displaySummary" :key="curr_index"></Example>
      <img v-if="examples.length > curr_index"   :src="isCorrect ? images.correct.src : images.wrong.src" 
      class="w-48 h-48 absolute t-50" :class="showIcon ? '' : 'hidden'" >
      
      <Summary v-if="showSummary" :total="total" :skipped="skipped" :mistakes="mistakes"></Summary>
    </div>

    
</template>
