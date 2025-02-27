<script setup>
import { useRecorderStore } from "@/stores/useRecorderStore";

const recorderStore = useRecorderStore();

const toggleRecording = () => {
  if (recorderStore.isRecording) {
    recorderStore.stopRecording();
  } else {
    recorderStore.startRecording();
  }
};

defineExpose({
  updateExampleData: recorderStore.updateExampleData,
});
</script>

<template>
  <div class="flex items-center justify-center">
    <button 
      @click="toggleRecording" 
      :class="recorderStore.isRecording ? 'bg-red-500 hover:bg-red-400' : 'bg-green-500 hover:bg-green-400'"
      class="w-24 h-24 flex items-center justify-center rounded-full text-white text-2xl focus:outline-none focus:ring-2 focus:ring-opacity-50"
      :title="recorderStore.isRecording ? 'Stop Recording' : 'Start Recording'"
    >
      <i :class="recorderStore.isRecording ? 'fas fa-stop' : 'fas fa-microphone'" class="text-4xl"></i>
    </button>
  </div>
</template>
