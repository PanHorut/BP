<!--
================================================================================
 Component: Subtopic.vue
 Description:
        Display subskill for main skill with example count - how many examples
        exist for selected combination of skills.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, defineProps, watch } from 'vue';
import { useLanguageStore } from '@/stores/useLanguageStore';
import { getSkillName } from '@/utils/dictionary';

const props = defineProps({
  subtopic: {
    required: true
  },
  selectedSubtopics: {
    type: Array,
    required: true
  }
});

const isSelected = ref(false);
const langStore = useLanguageStore();

// Select or deselect the subtopic skill
watch(isSelected, (newValue) => {

  // Selected
  if (newValue) {
    // Add to selected skills
    if (!props.selectedSubtopics.some(selected => selected.id === props.subtopic.id)) {
      props.selectedSubtopics.push(props.subtopic);
    }
  // Deselected
  } else {
    // Remove from selected skills
    removeFromSelection(props.subtopic);

    // Remove all skills children from selected skills
    removeChildrenFromSelection(props.subtopic.subskills);
  }
});

// Remove skill from selected skills
const removeFromSelection = (subtopic) =>{
  const index = props.selectedSubtopics.findIndex(
    (selected) => selected.id === subtopic.id);
  if (index !== -1) {
    props.selectedSubtopics.splice(index, 1);
  }
}

// Remove all skills children from selected skills
const removeChildrenFromSelection = (subskills) => {
  subskills.forEach(subskill => {
    removeFromSelection(subskill);
    if (subskill.subskills.length > 0) {
      removeChildrenFromSelection(subskill.subskills); 
    }
  });
}
// Get correct form of the word 'priklad' or 'example' depending on language used
const getCorrectForm = (count) => {

  if (langStore.language === 'en') {
    return count === 1 ? 'example' : 'examples';

  } else {
    if (count === 1) {
      return 'příklad';
    } else if (count > 1 && count < 5) {
      return 'příklady';
    } else {
      return 'příkladů';
    }
  }
}
</script>

<template>

  <div v-if="subtopic" class="pl-4 my-4">

    <div class="flex items-center justify-between mb-2">

      <!-- Subskill -->
      <label class="flex items-center space-x-2">

        <!-- Select checkbox -->
        <input 
          type="checkbox" 
          v-model="isSelected" 
          class="h-8 w-8  rounded text-primary border-gray-500 focus:ring-2 focus:ring-primary"
        />

        <!-- Subskill name and example count -->
        <span class="font-medium text-2xl">{{ getSkillName(subtopic.name, langStore.language) }}</span>
        <span class="text-lg text-gray-500">({{ subtopic.examples }} {{ getCorrectForm(subtopic.examples) }})</span>

      </label>
    </div>

    <!-- Subskills children -->
    <div v-if="subtopic.subskills.length > 0 && isSelected" class="subskills-list ml-6">

      <SubTopic 
        v-for="(subskill, index) in subtopic.subskills" 
        :key="index" 
        :subtopic="subskill" 
        :selectedSubtopics="selectedSubtopics"
      />

    </div>

  </div>
  
</template>