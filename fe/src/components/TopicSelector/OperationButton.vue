<!--
================================================================================
 Component: OperationButton.vue
 Description:
        Display operation skill and allow user to select it.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { defineProps, ref, computed, defineEmits } from 'vue';
import { useLanguageStore } from '@/stores/useLanguageStore';
import { getSkillName } from '@/utils/dictionary';

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

// Change count of examples in related subtopics example count
const emit = defineEmits(['updateExampleCount']);

const langStore = useLanguageStore();

// Select or deselect the operation skill
const select = () => {

  // Toggle selection
  isSelected.value = !isSelected.value;

  // Selected
  if (isSelected.value) {
    // Add to selected skills
    if (!props.selectedSubtopics.some(selected => selected.id === props.operation.id)) {
      props.selectedSubtopics.push(props.operation);
    }
  // Deselected
  } else {
    // Remove from selected skills
    removeFromSelection(props.operation);
  }
  
  // Change example counts of related examples 
  emit('updateExampleCount', { relatedSkills: props.operation.related_skills, isSelected: isSelected.value });
};

// Remove skill from selected skills
const removeFromSelection = (subtopic) => {
  const index = props.selectedSubtopics.findIndex(selected => selected.id === subtopic.id);
  if (index !== -1) {
    props.selectedSubtopics.splice(index, 1);
  }
};

// Style of button depending if selected or not
const buttonClasses = computed(() => ({
  'text-white bg-primary border-primary shadow-lg font-semibold transform': isSelected.value,
  'bg-gray-200 text-gray-800 border-gray-300 hover:bg-gray-300': !isSelected.value,
  'px-2 py-3 rounded-full border transition-all': true
}));
</script>

<template>

  <button @click="select" :class="buttonClasses" class="hover:shadow-md active:scale-95 text-xl">
    {{ getSkillName(operation.name, langStore.language) }}
  </button>
  
</template>
