<script setup>
import { ref, defineProps, defineEmits, nextTick, onMounted } from 'vue';
import ExampleCreator from './ExampleCreator.vue';
import WordProblemCreator from './WordProblemCreator.vue';
import { postTask } from '@/api/apiClient';
import { useToastStore } from '@/stores/useToastStore';
import { useTaskStore } from '@/stores/useTaskStore';
import { useRouter } from 'vue-router';

const props = defineProps({
  selectedSkills: {
    type: Array,
    default: () => []
  },
  inputType: {
    type: String
  },
  taskName: {
    type: String,
    default: "Cvičení"
  },
  examplesType: {
    type: String,
    default: "classic"
  }
});

const emit = defineEmits(['importTask', 'submit']);

const exampleCount = ref(10);  
const examples = ref([]);
const exampleCreators = ref([]);

const isExportOpen = ref(false);
const isImportOpen = ref(false);

const taskJSON = ref();
const task = ref();
const taskId = ref();

const validJSON = ref(false);

const toastStore = useToastStore();
const taskStore = useTaskStore();
const router = useRouter();

const edit = ref(false);
      
const addExampleCreators = () => {
  exampleCount.value += 6;
};

const collectExamples = (action) => {
  examples.value = [];

  exampleCreators.value.forEach((creator) => {
    if (creator) {
      const data = creator.getData();
      if (data !== null) examples.value.push(data);
    }
  });
  submitExamples(action);
};

const clearExamples = () => {
  exampleCreators.value.forEach((creator) => {
    if (creator) {
      creator.clearInput();
    }
  });
}

const submitExamples = async (action) => {
  try{

    if(props.selectedSkills.length === 0){
      toastStore.addToast({
        message: 'Nebyly vybrány žádné dovednosti',
        type: 'error',
        visible: true,
      });
      return;

    } else if(props.taskName === ''){
      toastStore.addToast({
        message: 'Nebyl vyplněn název sady',
        type: 'error',
        visible: true,
      });
      return;
    }
    await postTask(examples, props.selectedSkills, props.taskName, taskId.value, props.examplesType, action);
    toastStore.addToast({
        message: action == 'create' ? 'Sada byla vytvořena' : 'Změny byly uloženy',
        type: 'success',
        visible: true,
    });
    emit('submit');
    clearExamples();
    router.push('/tasks');


  }catch(error){
    toastStore.addToast({
        message: action == 'create' ? 'Sadu se nepodařilo vytvořit' : 'Změny se nepodařilo uložit',
        type: 'error',
        visible: true,
    });
  }
};

const exportJSON = () => {
  exampleCreators.value.forEach((creator) => {
    if (creator) {
      const data = creator.getData();
      if (data !== null) examples.value.push(data);
    }
  });

  task.value = { 'task_name': props.taskName, 'form': props.examplesType, 'skill_ids': props.selectedSkills, 'examples': examples };
  taskJSON.value = JSON.stringify(task.value, null, 2);

  isExportOpen.value = true;
};

const importJSON = () => {
  isImportOpen.value = false;

  if (task.value && task.value.examples) {
    const importedExamples = task.value.examples;
    const importedCount = importedExamples.length;

    // Adjust exampleCount based on the imported examples
    if (importedCount > exampleCount.value) {
      exampleCount.value = importedCount;
    }

    // Import examples into ExampleCreator components
    nextTick(() => {
      let index = 0;
      exampleCreators.value.forEach((creator) => {
        const example = importedExamples[index];
        if (creator && example) {
          creator.importExample(example.example, null, example.answer, example.steps);
          index++;
        }
      });
    });

    // Import task name and skills
    
    emit('importTask', task.value.task_name, task.value.skill_ids, task.value.form);
  }
};

const closeExportWindow = () => {
  examples.value = [];
  isExportOpen.value = false;
};

const toggleImportWindow = () => {
  isImportOpen.value = !isImportOpen.value;
};

const copyToClipboard = () => {
  if (taskJSON.value) {
    navigator.clipboard.writeText(taskJSON.value).then(
      () => { },
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

const importTask = () => {

  const task = taskStore.task;
  taskId.value = task.task_id;
  const skills = taskStore.skills;
  
    const importedExamples = task.examples;
    const importedCount = importedExamples.length;

    // Adjust exampleCount based on the imported examples
    if (importedCount > exampleCount.value) {
      exampleCount.value = importedCount;
    }

    // Import examples into ExampleCreator components
    nextTick(() => {
      let index = 0;
      exampleCreators.value.forEach((creator) => {
        const example = importedExamples[index];
        if (creator && example) {
          creator.importExample(example.example, example.example_id, example.answers[0].answer_text, example.steps);
          index++;
        }
      });
    });
    emit('importTask', task.task_name, skills, task.task_form);
  
};



onMounted(() => {
  if(taskStore.task){
    edit.value = true;
    importTask();
    taskStore.setTask(null, []);
  }
});
</script>

<template>
  <div class="flex flex-col items-center w-full">
    <div class="flex">
      <div @click="exportJSON" class="p-2 border-2 border-primary bg-primary text-white font-bold absolute right-4 top-32 rounded-md cursor-pointer">EXPORT</div>
      <div @click="toggleImportWindow" class="p-2  border-2 border-primary text-primary font-bold absolute right-28 top-32 rounded-md cursor-pointer">IMPORT</div>
    </div>
    <div v-if="props.examplesType == 'classic'" class="justify-center mt-12 grid grid-cols-1 xl:grid-cols-2 gap-4">
      <ExampleCreator
        v-for="index in exampleCount"
        :key="index"
        :number="index"
        ref="exampleCreators"
      />
    </div>
    <div v-else class="justify-center mt-12 grid grid-cols-1 gap-4 w-full">
      <WordProblemCreator
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
      v-if="edit"
      @click="collectExamples('edit')"
      class="p-4 my-6 flex justify-center items-center rounded-lg bg-secondary text-white font-black text-2xl cursor-pointer"
    >
      Uložit změny
    </div>
    <div
      v-else
      @click="collectExamples('create')"
      class="p-4 my-6 flex justify-center items-center rounded-lg bg-secondary text-white font-black text-2xl cursor-pointer"
    >
      Vytvořit cvičení
    </div>
  </div>

  <!-- TASK EXPORTER -->
  <div v-if="isExportOpen" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50 ">
    <div class="bg-white rounded-lg shadow-lg w-6/12 p-5 flex flex-col items-center">
        <div class=" flex justify-end items-center w-full">

          <div @click="copyToClipboard" class="p-2 rounded-md bg-secondary text-white font-semibold text-xl cursor-pointer mr-4">Copy</div>
          <div @click="closeExportWindow" class="p-2 rounded-md bg-slate-300 font-semibold text-xl cursor-pointer">Close</div>
        </div>
        <div class="overflow-y-auto max-h-[70vh]">
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
      <div class="flex flex-col gap-4 items-center mt-4 max-h-96 ">
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
