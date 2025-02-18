<script setup>
import { ref, defineProps, watch } from 'vue';

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

watch(isSelected, (newValue) => {
  if (newValue) {
    if (!props.selectedSubtopics.some(selected => selected.id === props.subtopic.id)) {
      props.selectedSubtopics.push(props.subtopic);
    }
  } else {
    removeFromSelection(props.subtopic);
    removeChildrenFromSelection(props.subtopic.subskills);
  }
});

const removeFromSelection = (subtopic) =>{
  const index = props.selectedSubtopics.findIndex(
    (selected) => selected.id === subtopic.id);
  if (index !== -1) {
    props.selectedSubtopics.splice(index, 1);
  }
}

const removeChildrenFromSelection = (subskills) => {
  subskills.forEach(subskill => {
    removeFromSelection(subskill);
    if (subskill.subskills.length > 0) {
      removeChildrenFromSelection(subskill.subskills); 
    }
  });
}
</script>

<template>
  <div v-if="subtopic" class="subtopic pl-4 my-4">
    <div class="flex items-center justify-between mb-2">
      <label class="flex items-center space-x-2">
        <input 
          type="checkbox" 
          v-model="isSelected" 
          class="h-6 w-6 rounded text-blue-600 border-gray-300 focus:ring-2 focus:ring-blue-500"
        />
        <span class="font-medium text-2xl">{{ subtopic.name }}</span>
        <span class="text-lg text-gray-500">({{ subtopic.examples }} příkladů)</span>
      </label>
    </div>

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
