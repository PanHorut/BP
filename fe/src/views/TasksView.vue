<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { getTasks, deleteExample, deleteTask } from '@/api/apiClient';
import { useTaskStore } from '@/stores/useTaskStore';
import { useToastStore } from '@/stores/useToastStore';
import { useRouter } from 'vue-router';
import Spinner from '@/components/Spinner.vue';

const tasks = ref([]);
const loading = ref(true);
const router = useRouter();
const toastStore = useToastStore();

const showDeleteModal = ref(false);
const taskToDelete = ref(null);
const taskToDeleteIndex = ref(null);
const taskToDeleteName = ref('');

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
  try {
    tasks.value = await getTasks();
  } catch (error) {
    console.error("Failed to fetch tasks:", error);
  } finally {
    loading.value = false;
  }
  nextTick(() => renderMathJax());
});

// Watch for changes in tasks and re-render MathJax
watch(tasks, () => {
  nextTick(() => renderMathJax());
});

// Open delete confirmation modal
const confirmDeleteTask = (taskId, taskIndex, taskName) => {
  taskToDelete.value = taskId;
  taskToDeleteIndex.value = taskIndex;
  taskToDeleteName.value = taskName;
  showDeleteModal.value = true;
};

// Cancel delete action
const cancelDelete = () => {
  taskToDelete.value = null;
  taskToDeleteIndex.value = null;
  taskToDeleteName.value = '';
  showDeleteModal.value = false;
};

// Method to handle the deletion of a task
const handleDeleteTask = async () => {
  if (!taskToDelete.value || taskToDeleteIndex.value === null) return;

  try {
    await deleteTask(taskToDelete.value);
    toastStore.addToast({
      message: `Sada "${taskToDeleteName.value}" byla smazána`,
      type: 'success',
      visible: true,
    });

    tasks.value.splice(taskToDeleteIndex.value, 1);
    console.log(`Task "${taskToDeleteName.value}" deleted successfully`);
  } catch (error) {
    console.error("Error deleting task:", error);
  } finally {
    cancelDelete();
  }
};

const handleEditTask = (taskIndex) => {
  const taskStore = useTaskStore();
  const task = tasks.value[taskIndex];
  const skills = tasks.value[taskIndex].examples[0].skills;
  taskStore.setTask(task, skills);

  router.push('/sandbox');
};
</script>

<template>
  <div class="max-w-4xl mx-auto p-4 pt-12">
    <div class="flex flex-col items-center justify-center">
      <h1 class="text-4xl text-primary font-bold text-center">Sady příkladů</h1>
      <RouterLink to="/sandbox"
        class="bg-green-500 hover:bg-green-700 p-4 cursor-pointer text-xl font-bold text-white rounded-lg my-4 transition">
        Vytvořit novou sadu
      </RouterLink>
      <Spinner v-if="loading" />
    </div>

    <div v-for="(task, taskIndex) in tasks" :key="task.task_id"
      class="border border-gray-300 rounded-lg shadow-sm p-4 mb-6 bg-white">
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
        <div class="flex">
          <button @click="handleEditTask(taskIndex)"
            class="bg-amber-500 hover:bg-amber-600 text-white text-sm py-1 px-3 rounded font-bold mr-4 transition"
            title="Upravit sadu">
            Upravit
          </button>
          <button @click="confirmDeleteTask(task.task_id, taskIndex, task.task_name)"
            class="bg-red-500 hover:bg-red-700 text-white text-sm py-1 px-3 rounded font-bold transition"
            title="Smazat celou sadu">
            Smazat
          </button>
        </div>
      </div>

      <details class="group">
        <summary class="cursor-pointer font-medium text-blue-600 hover:underline">
          Zobrazit příklady
        </summary>
        <div class="mt-4">
          <!-- Examples -->
          <div v-for="example in task.examples" :key="example.example_id"
            class="flex justify-between items-center mb-4 border-b pb-2">
            <p class="text-gray-700">
              <span>Příklad:</span> <span v-html="example.example" class="font-semibold text-black"></span>
            </p>

            <p class="text-gray-700">
              <span>Výsledek: </span>
              <span v-html="example.answers.map(a => a.answer_text).join(', ')" class="font-semibold text-black"></span>
            </p>
          </div>
        </div>
      </details>
    </div>
  </div>

  <!-- Delete Confirmation Modal -->
  <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-2xl  mb-4">Opravdu chcete smazat sadu <span class="font-semibold">{{ taskToDeleteName }}</span>?</h2>
      <p class="mt-2 text-lg font-semibold text-red-600"><i class="fa-solid fa-triangle-exclamation text-xl"></i> Tato akce je nevratná </p>
      <div class="flex justify-end gap-3 mt-4 font-semibold text-xl">
        <button @click="cancelDelete"
          class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400">
          Zrušit
        </button>
        <button @click="handleDeleteTask"
          class="px-4 py-1 bg-red-500 text-white rounded-lg hover:bg-red-600 transition font-semibold">
          Smazat
        </button>
      </div>
    </div>
  </div>
</template>
