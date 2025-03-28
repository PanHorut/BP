<script setup>
import { useRecorderStore } from "@/stores/useRecorderStore";
import SpeechVisualizer from './SpeechVisualizer.vue';
import { ref } from "vue";

const recorderStore = useRecorderStore();
const showConfirmation = ref(false);

const toggleRecording = () => {
  if (!recorderStore.allowedRecording && !recorderStore.isRecording) {
    showConfirmation.value = true;
    return;
  }

  if (recorderStore.isRecording) {
    recorderStore.stopRecording();
  } else {
    recorderStore.startRecording(false);
  }
};

const confirmRecording = () => {
  recorderStore.allowRecording(); 
  showConfirmation.value = false;
  recorderStore.startRecording(false);
};

const closeDialog = () => {
  showConfirmation.value = false;
};

defineExpose({
  updateExampleData: recorderStore.updateExampleData,
});
</script>

<template>
  <div class="flex flex-col md:flex-row items-center justify-center">
    <!-- Recording Button -->
    <button @click="toggleRecording"
      :class="recorderStore.isRecording ? 'bg-red-500 hover:bg-red-600 border-red-600' : 'bg-green-500 hover:bg-green-600 border-green-600'"
      class="w-24 h-24 flex items-center justify-center rounded-full border-4 text-white text-2xl focus:outline-none transition hover:scale-110 shadow-md z-10"
      :title="recorderStore.isRecording ? 'Stop Recording' : 'Start Recording'">
      <i :class="recorderStore.isRecording ? 'fas fa-stop' : 'fas fa-microphone'" class="text-4xl"></i>
    </button>

    <!-- Speech Visualizer -->
    <SpeechVisualizer class="mt-4 md:mt-0 md:ml-6 absolute md:relative z-0"
      :barColor="recorderStore.isRecording ? '#457b9d' : '#f1faee'" :width="300" :height="100" :barWidth="10"
      :barGap="8" :barCount="10" />
    <!-- Confirmation Dialog -->
    <div v-if="showConfirmation" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white p-12 rounded-lg shadow-xl w-2/3  md:w-1/2 text-center">
        <p class=" text-lg font-semibold mb-10 md:mb-20 md:text-2xl">Během zadávání výsledků hlasem budou pro zlepšení
          této aplikace Vaše hlasové odpovědi
          ukládány</p>
        <div class="flex flex-col md:flex-row justify-center">
          <button @click="confirmRecording"
            class="text-xl px-6 py-2 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition md:mr-6 mb-2 md:mb-0">
            Souhlasím
          </button>
          <button @click="closeDialog"
            class="text-xl px-6 py-2 bg-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-400 transition">
            Nesouhlasím
          </button>
        </div>

      </div>
    </div>
  </div>
</template>
