<script setup>
import { ref, defineProps } from 'vue';
import ExampleCreator from './ExampleCreator.vue';
import axios from 'axios';

const props = defineProps({
  selectedSkills: {
    type: Array,
    default: () => []
  },

  inputType:{
    type: String
  },

  taskName:{
    type: String,
    default: "Cvičení"
  }
});

const exampleCount = ref(10);
const examples = ref([]);
const exampleCreators = ref([]); 

const addExampleCreators = () => {
  exampleCount.value += 6;
};

const collectExamples = () => {
  examples.value = [];

  exampleCreators.value.forEach((creator) => {
    if (creator) {
      const data = creator.getData();
      if (data !== null) examples.value.push(data);
    }
  });
  
  submitExamples();
};

const submitExamples = async () => {
  console.log("Submitting examples:", examples.value);
  console.log("Selected skills:", props.selectedSkills);

  try {
    for (const example of examples.value) {
      const response = await axios.post('http://localhost:8000/api/add-example/', {
        example: example.example, 
        answer: example.answer,
        input_type: example.input_type,         
        skill_ids: props.selectedSkills.map(skill => skill.id), 
        task_name: props.taskName
      });
      
      console.log('Example added:', response.data);
    }
    
    console.log('All examples added successfully!');
  } catch (error) {
    if (error.response) {
      console.error('Error adding example:', error.response.data);
    } else {
      console.error('Network or server error:', error.message);
    }
  }
};

</script>

<template>
  <div class="flex flex-col items-center">
    <div class="justify-center mt-20 grid grid-cols-1 lg:grid-cols-2 gap-4">
      <ExampleCreator
        v-for="index in exampleCount"
        :key="index"
        :number="index"
        ref="exampleCreators" 
      />
    </div>

    <div @click="addExampleCreators" class="my-10 flex justify-center items-center rounded-full w-16 h-16 bg-secondary text-white font-black text-2xl">
      +
    </div>

    <div
      @click="collectExamples"
      class="p-4 my-6 flex justify-center items-center rounded-lg bg-secondary text-white font-black text-2xl cursor-pointer"
    >
      Vytvořit cvičení
    </div>
  </div>
</template>
