<script setup>
import Example from '@/components/Example.vue';
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import qs from 'qs';

const examples = ref([]);
const curr_index = ref(0);
const receivedAnswer = ref('');
const route = useRoute();
const topics = ref([]);

const checkAnswer = async (data) => {
  receivedAnswer.value = data;

  if (curr_index.value >= 0 && curr_index.value < examples.value.length) {
    if (receivedAnswer.value === examples.value[curr_index.value].answer) {
      curr_index.value++;
      console.log("Correct answer! Moving to the next example.");

      await nextTick(); 
    } else {
      console.log("Incorrect answer.");
    
    }
  } else {
    console.error("index is out of bounds:", curr_index.value);
  }
};

const fetchExamples = async (selectedIds) => {
  try {
    const response = await axios.get('http://localhost:8000/api/examples/', {
      params: {
        skill_ids: selectedIds, 
      },
      paramsSerializer: (params) => {
        return qs.stringify(params, { arrayFormat: 'repeat' }); 
      },
    });
    examples.value = response.data; 
    console.log("Fetched examples:", examples.value); 
  } catch (error) {
    console.error("Error fetching examples:", error);
  }
};



onMounted(() => {
  if (route.query.topics) {
    topics.value = JSON.parse(route.query.topics);
    fetchExamples(topics.value);
  }

});
</script>

<template>

    <Example v-if="examples.length > curr_index" :example="examples[curr_index]" @answerSent="checkAnswer" :key="curr_index"></Example>
    <div v-else class="flex justify-center">
    <RouterLink to="/"  class="text-center text-4xl mt-20 border-4 border-blue-600 p-5 rounded-3xl cursor-pointer">Zpět na hlavní stránku</RouterLink>
    </div>
</template>
