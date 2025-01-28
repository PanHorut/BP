<script setup>
import {ref, onMounted} from 'vue';
import TopicCard from '@/components/MainMenu/TopicCard.vue';
import { getParentSkills } from '@/api/apiClient';
import Spinner from '../Spinner.vue';

const topics = ref([]) 
const loading = ref(true);  

onMounted(async () => {
  try {
    topics.value = await getParentSkills();
  } catch (error) {
    console.error("Failed to fetch topics:", error);
  } finally {
    loading.value = false;
  }
  
})

</script>

<template>
    <Spinner v-if="loading" class="mt-48"/>

    <div class="flex justify-center p-11">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-x-20 gap-y-10">
        <TopicCard 
        v-for="(topic, index) in topics" 
        :key="index" 
        :topic="topic.name" 
        :id="Number(topic.id)"
      />
        
      </div>
    </div>
  </template>