<script setup>
import Example from '@/components/Example.vue';
import { ref, onMounted } from 'vue';

import axios from 'axios';

const examples = ref([]);
const curr_index = ref(0);

const receivedAnswer = ref('');

const checkAnswer = (data) => {
    receivedAnswer.value = data;

    if (curr_index.value >= 0 && curr_index.value < examples.value.length) {
        
        if (receivedAnswer.value === examples.value[curr_index.value].answer) {
            curr_index.value++;
        
        } else {
           
        }
    } else {
        console.error("Current index is out of bounds:", curr_index.value);
    }
}

const fetchExamples = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/examples/');  
    examples.value = response.data;  
    
} catch (error) {
    console.error('Error fetching examples:', error);  
  }
};

onMounted(() => {
  fetchExamples(); 
});

</script>

<template>

    <Example v-if="examples.length > curr_index" :example="examples[curr_index].example" @answerSent="checkAnswer"></Example>
    <div v-else class="flex justify-center">
    <RouterLink to="/"  class="text-center text-4xl mt-20 border-4 border-blue-600 p-5 rounded-3xl cursor-pointer">Zpět na hlavní stránku</RouterLink>
    </div>
</template>
