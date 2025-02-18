<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { getTasks, deleteExample, deleteTask } from '@/api/apiClient'; // Adjust the path to match your project structure
import { useTaskStore } from '@/stores/useTaskStore';
import { useRouter } from 'vue-router';
import Spinner from '@/components/Spinner.vue';

const tasks = ref([]);
const loading = ref(true);
const router = useRouter(); 


// Function to render MathJax content
const renderMathJax = () => {
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise().catch((err) =>
      console.error('MathJax rendering error:', err)
    );
  } else {
    console.warn('MathJax is not loaded properly');
  }
};

// Fetch tasks and render MathJax when tasks update
onMounted(async () => {
  try{
    tasks.value = await getTasks();
  } catch (error) {
    console.error("Failed to fetch tasks:", error);
  } finally {
    loading.value = false;
  }
  nextTick(() => renderMathJax()); // Render MathJax after the DOM updates
});

// Watch for changes in tasks and re-render MathJax
watch(tasks, () => {
  nextTick(() => renderMathJax());
});

// Method to handle the deletion of an example
const handleDeleteExample = async (exampleId, taskIndex) => {
  try {
    // Call the delete API
    await deleteExample(exampleId);

    // Remove the example from the local tasks data
    const task = tasks.value[taskIndex];
    task.examples = task.examples.filter(example => example.example_id !== exampleId);
    console.log(`Example with ID ${exampleId} deleted successfully`);
  } catch (error) {
    console.error("Error deleting example:", error);
  }
};

// Method to handle the deletion of a task
const handleDeleteTask = async (taskId, taskIndex) => {
  try {
    await deleteTask(taskId);

    // Remove the task from the local tasks data
    tasks.value.splice(taskIndex, 1);
    console.log(`Task with ID ${taskId} deleted successfully`);
  } catch (error) {
    console.error("Error deleting task:", error);
  }
};

const handleEditTask = (taskIndex) => {
  const taskStore = useTaskStore();
  const task = tasks.value[taskIndex]
  const skills = tasks.value[taskIndex].examples[0].skills;
  taskStore.setTask(task, skills);

  router.push('/sandbox');
}
</script>

<template>


    <div class="max-w-4xl mx-auto p-4 pt-12">
        <div class="flex flex-col items-center justify-center">
            <h1 class="text-4xl text-primary font-bold text-center">Sady příkladů</h1>
            <RouterLink to="/sandbox" class="bg-green-500 hover:bg-green-700 p-4 cursor-pointer text-xl font-bold text-white rounded-lg my-4 transition">
                Vytvořit novou sadu
            </RouterLink>
            <Spinner v-if="loading" />
        </div>
  
      <div
        v-for="(task, taskIndex) in tasks"
        :key="task.task_id"
        class="border border-gray-300 rounded-lg shadow-sm p-4 mb-6 bg-white"
      > 
        <!-- Task Name -->
        <div class="flex justify-between items-start">
            <div class="flex flex-col">
            <h2 class="text-lg font-semibold mb-2">
                {{ task.task_name }}
            </h2>
    
            <!-- Render skills only for the first example -->
            <span v-if="task.examples.length > 0">
                <span v-for="skill in task.examples[0].skills" :key="skill.id" class="mr-2 text-sm text-gray-600">
                    {{ skill.name }}
                </span>
            </span>

            
            </div>

          <!-- Smazat Task Button -->

          <div class="flex">
          <button
            @click="handleEditTask(taskIndex)"
            class="bg-amber-500 hover:bg-amber-600 text-white text-sm py-1 px-3 rounded font-bold mr-4 transition"
            title="Upravit sadu"
          >
            Upravit
          </button>
          <button
            @click="handleDeleteTask(task.task_id, taskIndex)"
            class="bg-red-500 hover:bg-red-700 text-white text-sm py-1 px-3 rounded font-bold transition"
            title="Smazat celou sadu"
          >
            Smazat
          </button>
          
          </div>

          
        </div>

        <!-- Dropdown for details -->
        <details class="group">
          <summary class="cursor-pointer font-medium text-blue-600 hover:underline">
            Zobrazit příklady
          </summary>
          <div class="mt-4">
            <!-- Examples -->
            <div
              v-for="example in task.examples"
              :key="example.example_id"
              class="flex justify-between items-center mb-4 border-b pb-2"
            >
              <!-- Render Example -->
              <p class="text-gray-700">
                <span>Příklad:</span> <span v-html="example.example" ref="exampleText" class="font-semibold text-black"></span>
              </p>
              
              <!-- Render Answer -->
              <p class="text-gray-700">
                <span>Výsledek: </span> 
                <span v-html="example.answers.map(a => a.answer_text).join(', ')" ref="answerText" class="font-semibold text-black"></span>
              </p>

              <!-- Delete Example Button (×) -->
              <button
                @click="handleDeleteExample(example.example_id, taskIndex)"
                class="bg-red-500 hover:bg-red-700 text-xl text-white w-8 h-8 rounded-lg"
                title="Delete Example"
              >
              <i class="fa-solid fa-xmark" style="color: #ffffff;"></i>
                          
            </button>
            </div>
          </div>
        </details>
   
      </div>
    </div>
  </template>
