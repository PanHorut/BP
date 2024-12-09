<script setup>
import {ref, onMounted} from 'vue';
import TopicCard from '@/components/MainMenu/TopicCard.vue';
import { getParentSkills } from '@/api/apiClient';

const topics = ref([]) 

onMounted(async () => {

    
    topics.value = getParentSkills();
  
})

</script>

<template>
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