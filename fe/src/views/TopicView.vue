<script setup>
import { ref, defineProps, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getSkill } from '@/api/apiClient';
import SubTopic from '@/components/SubTopic.vue';
  
const props = defineProps({
    id: {
    type: Number,
    required: true
    }
  })

const topic = ref(null);
const subtopics = ref([]);
const selectedSubtopics = ref([]);


onMounted(async () => {
    const response = await getSkill(props.id);
    topic.value = response.skill;
    subtopics.value = response.child_skills;

})

const handleToggle = ({ id, checked }) => {
  if (checked) {
    selectedSubtopics.value.push(id); 
  } else {
    selectedSubtopics.value.splice(id, 1); 
  }
};

const router = useRouter()

function startPracticing() {
    router.push({ name: 'examples', query: { topics: JSON.stringify(selectedSubtopics.value) } });
}


</script>

<template>
    <div class="flex flex-col items-center">
      <h1 class="text-4xl font-bold text-primary my-8" v-if="topic">{{ topic.name }}</h1>
      <p class="text-secondary text-xl">Vyberte, co vše chcete procvičit</p>
      <div class="flex my-8">
        <SubTopic 
          v-for="(subtopic, index) in subtopics" 
          :key="index" 
          :subtopic="subtopic" 
          @toggle="handleToggle" 
          class="mr-8" 
        />
      </div>
      <div @click="startPracticing" 
        class="cursor-pointer bg-tertiary px-6 py-3 rounded-2xl font-bold text-primary text-2xl">
        Začít procvičovat
    </div>
    </div>
</template>
