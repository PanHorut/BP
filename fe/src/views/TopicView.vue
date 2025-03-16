<script setup>
import { ref, defineProps, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getSkill, getRelatedSkillsTree, getChildrenSkillsTree, getOperationSkills } from '@/api/apiClient';
import Spinner from '@/components/Spinner.vue';
import OperationButton from '@/components//TopicSelector/OperationButton.vue';
import SubTopic from '@/components/TopicSelector/SubTopic.vue';

const props = defineProps({
  id: {
    required: true
  }
});

const topic = ref(null);
const subtopics = ref([]);
const selectedSubtopics = ref([]);
const operations = ref([]);
const noTopics = ref(false);
const loading = ref(true);

onMounted(async () => {
  try {
    topic.value = await getSkill(props.id);

    if(topic.value.skill_type === 'OPERATION') {
      subtopics.value = await getRelatedSkillsTree(props.id);
      console.log(subtopics.value);
    } else if(topic.value.skill_type === 'NUMBER_DOMAIN') {
      subtopics.value = await getChildrenSkillsTree(props.id, false);
      operations.value = await getOperationSkills(props.id);
      console.log(operations.value);
      console.log(subtopics.value);
    } else if(topic.value.skill_type === 'EQUATION') {
      subtopics.value = await getChildrenSkillsTree(props.id, true);
    } 

    selectedSubtopics.value.push(topic.value);

  } catch (error) {
    console.error("Failed to fetch skill data:", error);
  } finally {
    loading.value = false;
  }
});

const router = useRouter();

function startPractice() {
  if (selectedSubtopics.value.length > 0) {
    router.push({
      name: 'examples',
      query: { 
        topics: JSON.stringify(selectedSubtopics.value.map(subtopic => subtopic.id)),
      }
    });
  } else {
    noTopics.value = true;
    setTimeout(() => {
      noTopics.value = false;
    }, 2000);
  }
}

const updateExampleCount = ({ relatedSkills, isSelected }) => {
  relatedSkills.forEach(({ related_id, examples }) => {
    const subtopic = subtopics.value.find(sub => sub.id === related_id);
    
    if (subtopic) {
      subtopic.examples += isSelected ? examples : -examples;
    }
  });
};



</script>

<template>
  <div class="flex flex-col items-center md:pt-20">
    <h1 class="text-5xl font-bold text-primary my-8" v-if="topic">
      {{ topic.name }}
    </h1>
    

    <Spinner v-if="loading" class="mt-24" />

    <!-- Render operations as buttons using the new component -->
    <p v-if="operations.length > 0" class="text-secondary font-semibold text-xl mt-8 mb-4">Vyber operace, které chceš procvičit</p>
    <div v-if="operations.length > 0" class="grid grid-cols-2 gap-4 mb-4 md:flex md:flex-row md:flex-wrap md:space-x-4 md:justify-start justify-center">
      <OperationButton 
        v-for="operation in operations" 
        :key="operation.id" 
        :operation="operation"
        :selectedSubtopics="selectedSubtopics"
        @updateExampleCount="updateExampleCount"
        class="md:w-auto w-full"

      />
    </div>

    <p v-if="subtopics.length > 0" class="text-secondary font-semibold text-xl mt-8 mb-4">Jaké příklady chceš procvičit? </p>
    <div v-if="subtopics.length > 0" class="flex flex-col md:flex-row ">
      <SubTopic
        v-for="subtopic in subtopics"
        :key="subtopic.id"
        :subtopic="subtopic"
        :selectedSubtopics="selectedSubtopics"
      />
    </div>

    <div @click="startPractice" class="my-20 px-6 py-3 bg-secondary text-4xl md:text-3xl font-bold text-white rounded-lg cursor-pointer hover:bg-primary transition">
      JDEME NA TO
    </div>
  </div>
</template>
