<script setup>
import Example from '@/components/Example.vue';
import ProgressBar from '@/components/Example/ProgressBar.vue';
import SpecialCharsBar from '@/components/Example/SpecialCharsBar.vue';
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { getExamples } from '@/api/apiClient';
import correctIcon from '@/assets/img/correct.png';
import wrongIcon from '@/assets/img/wrong.png'

const examples = ref([]); 
const curr_index = ref(0); 
const route = useRoute();
const topics = ref([]);

const isCorrect = ref(false);
const showIcon = ref(false);


const displayNext = async (isCorrect) => {

  if (curr_index.value >= 0 && curr_index.value < examples.value.length) {
    
    if (isCorrect) {
      displayIcon(true);
      
      curr_index.value++;
      await nextTick(); 
    } else {
      displayIcon(false);
      console.log("Incorrect answer.");
    }
  } else {
    console.error("index is out of bounds:", curr_index.value);
  }
};

const fetchExamples = async (selectedIds) => {
  
    examples.value = await getExamples(selectedIds);
 
};

const displayIcon = (correct) => {
  isCorrect.value = correct;
  showIcon.value = true;

  setTimeout(() => {
    showIcon.value = false;
  }, 250);
};

onMounted(() => {
  if (route.query.topics) {
    topics.value = JSON.parse(route.query.topics);
    fetchExamples(topics.value);
  }
});
</script>

<template>
    <SpecialCharsBar></SpecialCharsBar>
    <div class="flex justify-center">
      <ProgressBar :totalExamples="examples.length" :finishedExamples="curr_index"></ProgressBar>
    </div>
    <div class="flex items-center justify-center">
      <Example v-if="examples.length > curr_index" :example="examples[curr_index]" :answer="examples[curr_index].answers[0].answer" @answerSent="displayNext" :key="curr_index"></Example>
      <img v-if="examples.length > curr_index" :src="isCorrect ? correctIcon : wrongIcon" class="w-36 h-36 ml-10 mb-40 self-end" :class="showIcon ? '' : 'hidden'" >
      <div v-else class="flex justify-center">
        <RouterLink to="/"  class="text-center text-4xl mt-20 border-4 border-blue-600 p-5 rounded-3xl cursor-pointer">Zpět na hlavní stránku</RouterLink>
      </div>
    </div>
</template>
