<script setup>
import { defineProps, ref, computed, defineEmits } from 'vue';

const props = defineProps({
  operation: {
    type: Object,
    required: true
  },
  selectedSubtopics: {
    type: Array,
    required: true
  }
});

const isSelected = ref(false);
const emit = defineEmits(['updateExampleCount']);


const select = () => {
  isSelected.value = !isSelected.value;

  if (isSelected.value) {
    if (!props.selectedSubtopics.some(selected => selected.id === props.operation.id)) {
      props.selectedSubtopics.push(props.operation);
    }
  } else {
    removeFromSelection(props.operation);
  }

  emit('updateExampleCount', { relatedSkills: props.operation.related_skills, isSelected: isSelected.value });
};

const removeFromSelection = (subtopic) => {
  const index = props.selectedSubtopics.findIndex(selected => selected.id === subtopic.id);
  if (index !== -1) {
    props.selectedSubtopics.splice(index, 1);
  }
};

// Computed styles
const buttonClasses = computed(() => ({
  'text-white bg-primary border-primary shadow-lg transform scale-105': isSelected.value,
  'bg-gray-200 text-gray-800 border-gray-300 hover:bg-gray-300': !isSelected.value,
  'px-5 py-3 rounded-full border transition-all duration-200 ease-in-out': true
}));
</script>

<template>
  <button @click="select" :class="buttonClasses" class="hover:shadow-md active:scale-95">
    {{ operation.name }}
  </button>
</template>
