<!--
================================================================================
 Component: Topics.vue
 Description:
        Displays landing page skills and search bar to filter them by name.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useTopicStore } from '@/stores/useMainpageTopicStore';
import TopicCard from '@/components/MainMenu/TopicCard.vue';
import Spinner from '../Spinner.vue';
import { useLanguageStore } from '@/stores/useLanguageStore';
import { dictionary } from '@/utils/dictionary';

// Load topics from cache
const topicStore = useTopicStore();
const langStore = useLanguageStore();

const searchQuery = ref('');

// Show only skills that match the search query
const filteredTopics = computed(() => {
  if (!searchQuery.value) return topicStore.topics;
  
  return topicStore.topics.filter(topic => 
    topic.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Get landing page skills
onMounted(() => {
  topicStore.fetchTopics();
});
</script>

<template>
  <div>
    
    <Spinner v-if="topicStore.loading" class="pt-48" />

    <!-- Search Bar -->
    <div v-if="langStore.language == 'cs'" class="flex justify-center px-4 pt-10 md:pt-20">
      <div class="relative w-full max-w-lg">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-xl">
          <i class="fa-solid fa-magnifying-glass"></i>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="dictionary[langStore.language].searchPlaceholderText"
          class="w-full pl-10 pr-4 py-3 rounded-xl bg-white border border-gray-200
                 shadow-sm focus:outline-none focus:ring-4 focus:ring-primary
                 focus:border-transparent transition duration-200 ease-in-out
                 text-gray-700 placeholder-gray-400"
        >
      </div>
    </div>

    <!-- Skills -->
    <div class="flex justify-center py-20 ">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-20 gap-y-10">
        <TopicCard 
          v-for="(topic, index) in filteredTopics" 
          :key="index" 
          :topic="topic.name" 
          :id="Number(topic.id)"
        />
      </div>
    </div>

  </div>
</template>