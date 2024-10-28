<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  subtopic: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits();

const isChecked = ref(false);

// This function toggles the checkbox state and emits the change
const toggleCheckbox = () => {
  isChecked.value = !isChecked.value; // Toggle the state
  emit('toggle', { id: props.subtopic.id, checked: isChecked.value }); // Emit the event with the current state
};
</script>

<template>
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
</template>
