<script setup>
import { ref, defineProps, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getSkill } from '@/api/apiClient';
import SubTopic from '@/components/SubTopic.vue';
import Spinner from '@/components/Spinner.vue';
  
const props = defineProps({
    id: {
    type: Number,
    required: true
    }
  })

const topic = ref(null);
const subtopics = ref([]);
const selectedSubtopics = ref([]);
const noTopics = ref(false);

const loading = ref(true);


onMounted(async () => {
  try {
    const response = await getSkill(props.id);
    topic.value = response.skill;
    subtopics.value = response.child_skills;
  } catch (error) {
    console.error("Failed to fetch skill data:", error);
  } finally {
    loading.value = false; 
  }

})

const handleToggle = ({ id, checked }) => {
  if (checked) {
    
    if (!selectedSubtopics.value.some((item) => item.id === id)) {
      selectedSubtopics.value.push({ id, count: 10 });
    }
    
  } else {
    const index = selectedSubtopics.value.findIndex((subtopic) => subtopic.id === id); 
    if (index !== -1) {
      selectedSubtopics.value.splice(index, 1);
    }
  }
};

const handleUpdateCount = ({ id, newCount }) => {
  const subtopic = selectedSubtopics.value.find((item) => item.id === id);
  if (subtopic) {
    subtopic.count = newCount; 
  }
};

const router = useRouter()

function startPractice() {

  if(selectedSubtopics.value.length > 0){
    router.push({ 
      name: 'examples', 
      query: { topics: JSON.stringify(selectedSubtopics.value) } 
    });
  }else {
    noTopics.value = true;

    setTimeout(() => {
      noTopics.value = false; 
    }, 2000);
  }
}


</script>

<template>

    <div class="flex flex-col items-center">
      <h1 class="text-4xl font-bold text-primary my-8" v-if="topic">{{ topic.name }}</h1>
      <p class="text-secondary text-xl">Vyberte, co vše chcete procvičit</p>

      <Spinner v-if="loading" class="mt-24"/>

      <div class="flex my-8">
        <SubTopic 
          v-for="(subtopic, index) in subtopics" 
          :key="index" 
          :subtopic="subtopic" 
          @toggle="handleToggle" 
          @updateCount="handleUpdateCount" 
          class="mr-8" 
        />
      </div>
      <div @click="startPractice" 
        class="cursor-pointer bg-tertiary px-6 py-3 rounded-2xl font-bold text-primary text-2xl">
        Začít procvičovat
      </div>

      <transition name="fade">
        <div 
          v-if="noTopics" 
          class="text-red-600 font-semibold text-xl mt-6">
            Nebylo vybráno žádné cvičení
        </div>
      </transition>   

    </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

</style>
