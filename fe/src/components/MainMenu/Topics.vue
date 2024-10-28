<script setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import TopicCard from '@/components/MainMenu/TopicCard.vue';

const topics = ref([]) 

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/parent-skills/');
    topics.value = response.data
  } catch (error) {
    console.error("Error fetching skills:", error)
  }
})

</script>

<template>
    <div class="flex justify-center p-11">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-x-20 gap-y-10">
        <TopicCard 
        v-for="(topic, index) in topics" 
        :key="index" 
        :topic="topic.name" 
        :id="topic.id"
      />
        
      </div>
    </div>
  </template>