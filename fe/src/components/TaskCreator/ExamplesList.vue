<script setup>
import { ref, defineProps, defineEmits } from 'vue';
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

const emit = defineEmits(['importTask']);

const exampleCount = ref(10);
const examples = ref([]);
const exampleCreators = ref([]); 

const isExportOpen = ref(false);
const isImportOpen = ref(false);

const taskJSON = ref();
const task = ref();

const validJSON = ref(false);

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

const exportJSON = () => {
  exampleCreators.value.forEach((creator) => {
    if (creator) {
      const data = creator.getData();
      if (data !== null) examples.value.push(data);
    }
  });

  task.value = {'task_name': props.taskName, 'skill_ids': props.selectedSkills, 'examples': examples};

  taskJSON.value = JSON.stringify(task.value, null, 2);
  console.log(taskJSON.value)

  isExportOpen.value = true;
  
}

const importJSON = () => {

  isImportOpen.value = false;
 
  const len = ref();
  
  if(length > 10){
    len.value = task.value.examples.length
    if(len % 2 === 0){
      exampleCount.value = len;
    }else{
      exampleCount.value = len + 1;
    }
  }
  
  // import examples
  const index = ref(0);
  exampleCreators.value.forEach((creator) => {
    const example = task.value.examples[index.value];
    
    if (creator && example) {
      creator.importExample(example.example, example.answer, example.steps)
      index.value++;
    }
  });

  // import task name and skills
  emit('importTask', task.value.task_name, task.value.skill_ids)
}


const closeExportWindow = () => {
  examples.value = [];
  isExportOpen.value = false;
}

const toggleImportWindow = () => {
  isImportOpen.value = !isImportOpen.value;
}

const copyToClipboard = () => {
  if (taskJSON.value) {
    navigator.clipboard.writeText(taskJSON.value).then(
      () => {
        
      },
      (err) => {
        console.error('Failed to copy JSON: ', err);
      }
    );
  }
};

const downloadJSON = () => {
  if (taskJSON.value) {
    const blob = new Blob([taskJSON.value], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `${props.taskName || 'task'}.json`;
    link.click();

    URL.revokeObjectURL(url);
  }
};

const handleJSON = (event) => {
  const file = event.target.files[0];

  if (file && file.type === 'application/json') {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const jsonData = JSON.parse(e.target.result); 
        task.value = jsonData; 
        validJSON.value = true; 
      } catch (err) {
        
        validJSON.value = false; 
      }
    };

    reader.readAsText(file); 
  } else {
    validJSON.value = false; 
  }
};
</script>

<template>
  <div class="flex flex-col items-center">
    <div class="flex">
      <div @click="exportJSON" class="p-2 border-2 border-primary bg-primary text-white font-bold absolute right-4 top-32 rounded-md cursor-pointer">EXPORT</div>
      <div @click="toggleImportWindow" class="p-2  border-2 border-primary text-primary font-bold absolute right-28 top-32 rounded-md cursor-pointer">IMPORT</div>
    </div>
    <div class="justify-center mt-20 grid grid-cols-1 xl:grid-cols-2 gap-4">
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

  <!-- TASK EXPORTER -->
  <div v-if="isExportOpen" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white rounded-lg shadow-lg w-6/12 p-5 flex flex-col items-center">
        <div class=" flex justify-end items-center w-full">

          <div @click="copyToClipboard" class="p-2 rounded-md bg-secondary text-white font-semibold text-xl cursor-pointer mr-4">Copy</div>
          <div @click="closeExportWindow" class="p-2 rounded-md bg-slate-300 font-semibold text-xl cursor-pointer">Close</div>
        </div>
        <div>
          <pre>{{ taskJSON }}</pre>
        </div>
        <div class="w-full flex justify-center mt-4">
          <div @click="downloadJSON" class="p-2 rounded-md bg-secondary text-white font-semibold text-xl cursor-pointer">Download</div>
        </div>
    </div>
  </div>

  <!-- TASK IMPORTER -->
  <div v-if="isImportOpen" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
  <div class="bg-white rounded-lg shadow-lg w-4/12 p-5 flex flex-col items-center">
    <div class="flex justify-end items-center w-full">
      <p @click="toggleImportWindow" class="p-2 rounded-md bg-slate-300 font-semibold text-xl cursor-pointer">
        Close
      </p>
    </div>
    <div class="flex flex-col gap-4 items-center mt-4">
      <input
        type="file"
        accept=".json"
        @change="handleJSON"
        class="border p-2 rounded-md cursor-pointer"
      />
    </div>
    <div v-if="validJSON" @click="importJSON" class="mt-4 p-2 rounded-md bg-secondary text-white font-semibold text-xl cursor-pointer">Import examples</div>
    </div>
  </div>


</template>


