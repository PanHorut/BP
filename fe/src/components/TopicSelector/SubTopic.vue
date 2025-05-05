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
      <label class="flex items-center space-x-2">
        <input 
          type="checkbox" 
          v-model="isSelected" 
          class="h-8 w-8  rounded text-primary border-gray-500 focus:ring-2 focus:ring-primary"
        />
        <span class="font-medium text-2xl">{{ getSkillName(subtopic.name, langStore.language) }}</span>
        <span class="text-lg text-gray-500">({{ subtopic.examples }} {{ getCorrectForm(subtopic.examples) }})</span>
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