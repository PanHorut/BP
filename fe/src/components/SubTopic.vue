<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  subtopic: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits();

const exampleCount = ref(10);
const isChecked = ref(false);

// This function toggles the checkbox state and emits the change
const toggleCheckbox = () => {
  isChecked.value = !isChecked.value; // Toggle the state
  emit('toggle', { id: props.subtopic.id, checked: isChecked.value }); // Emit the event with the current state
};

const updateCount = () => {
  emit('updateCount', { id: props.subtopic.id, newCount: Number(exampleCount.value) });
};
</script>

<template>
  <div class="flex flex-col space-y-4">
    <!-- Name of subtopic and checkbox -->
    <div class="flex items-center space-x-2">
      <input 
        type="checkbox" 
        :id="subtopic.id" 
        class="w-8 h-8 text-blue-600 border-gray-300 rounded focus:ring-blue-500" 
        :checked="isChecked"  
        @change="toggleCheckbox" 
      />
      <label :for="subtopic.id" class="text-2xl">{{ subtopic.name }}</label>
    </div>
    
    <!-- Slider -->
    <div v-if="isChecked" class="flex flex-col items-center space-y-2">
      <label for="example-slider" class="text-lg">{{ exampleCount }} {{ exampleCount == 1 ? 'příklad' : 'příkladů'}}</label>
      <input 
        type="range" 
        min="1" 
        max="50" 
        step="1" 
        v-model="exampleCount" 
        class="w-full" 
        @input="updateCount" 
      />
    </div>
  </div>
</template>
