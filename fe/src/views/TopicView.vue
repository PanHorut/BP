<!--
================================================================================
 Component: TopicView.vue
 Description:
      Displays selected skill related skills and children to allow user to specify all 
      skills he wants to practice.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, defineProps, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Spinner from '@/components/Spinner.vue';
import OperationButton from '@/components//TopicSelector/OperationButton.vue';
import SubTopic from '@/components/TopicSelector/SubTopic.vue';
import { dictionary, getSkillName } from '@/utils/dictionary';
import { useLanguageStore } from '@/stores/useLanguageStore';
import { useSkillStore } from '@/stores/useSkillStore';

const props = defineProps({
  id: {
    required: true
  }
});

const topic = ref(null);
const subtopics = ref([]);
const operations = ref([]);

const selectedSubtopics = ref([]);
const loading = ref(true);

// Dictionary to support both czech and english version
const langStore = useLanguageStore();

// Used for caching skills
const skillStore = useSkillStore();

const router = useRouter();

onMounted(async () => {
  try {
    
    // Fetch main skill
    topic.value = await skillStore.fetchSkill(props.id);

    // Fetch subskills based on the type of the main skill
    if (topic.value.skill_type === 'OPERATION') {
      // Fetch associated skills
      subtopics.value = await skillStore.fetchRelatedSkillsTree(props.id);

    } else if (topic.value.skill_type === 'NUMBER_DOMAIN') {
      // Fetch both subskills and associated operations skills
      subtopics.value = await skillStore.fetchChildrenSkillsTree(props.id, false);
      operations.value = await skillStore.fetchOperationSkills(props.id);

    } else if (topic.value.skill_type === 'EQUATION') {
      // Fetch subskills
      subtopics.value = await skillStore.fetchChildrenSkillsTree(props.id, true);
    }

    selectedSubtopics.value.push(topic.value);

  } catch (error) {
    console.error("Failed to fetch skill data:", error);
  } finally {
    loading.value = false;
  }
});

// Pass selected skills to retrieve examples and start practice
function startPractice() {
  if (selectedSubtopics.value.length > 0) {
    router.push({
      name: 'examples',
      query: {
        topics: JSON.stringify(selectedSubtopics.value.map(subtopic => subtopic.id)),
      }
    });

  }
}

// Update example counts of subskills
const updateExampleCount = ({ relatedSkills, isSelected }) => {
  relatedSkills.forEach(({ related_id, examples }) => {
    const subtopic = subtopics.value.find(sub => sub.id === related_id);

    if (subtopic) {
      // Increment or decrement the example count based on selection
      subtopic.examples += isSelected ? examples : -examples;
    }
  });
};
</script>

<template>

  <div class="flex flex-col items-center md:pt-20">

    <!-- Main skill name -->
    <h1 class="text-5xl font-bold text-primary my-8 text-center" v-if="topic">
      {{ getSkillName(topic.name, langStore.language) }}
    </h1>


    <Spinner v-if="loading" class="mt-24" />

    <p v-if="operations.length > 0" class="text-secondary font-semibold text-xl text-center mt-8 mb-4">
      {{ dictionary[langStore.language].chooseOperation }}
    </p>

    <!-- Operations skills -->  
    <div v-if="operations.length > 0"
      class="grid grid-cols-2 gap-4 mb-4 md:flex md:flex-row md:flex-wrap md:space-x-4 md:justify-start justify-center">
      <OperationButton v-for="operation in operations" :key="operation.id" :operation="operation"
        :selectedSubtopics="selectedSubtopics" @updateExampleCount="updateExampleCount" class="md:w-auto w-full" />
    </div>

    <p v-if="subtopics.length > 0" class="text-secondary font-semibold text-xl text-center mt-8 mb-4">
      {{dictionary[langStore.language].chooseTopic }}
    </p>

    <!-- Subskills -->
    <div v-if="subtopics.length > 0" class="flex flex-wrap justify-center gap-4">
      <SubTopic v-for="subtopic in subtopics" :key="subtopic.id" :subtopic="subtopic"
        :selectedSubtopics="selectedSubtopics" />
    </div>

    <!-- Button to start practice --> 
    <div @click="startPractice"
      class="my-20 px-6 py-3 bg-secondary text-4xl md:text-3xl font-bold text-white rounded-lg cursor-pointer hover:bg-primary transition">
      {{ dictionary[langStore.language].startPractice }}
    </div>

  </div>

</template>
