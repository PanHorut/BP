<script setup>
import { onMounted } from 'vue';
import { useTopicStore } from '@/stores/useMainpageTopicStore';
import TopicCard from '@/components/MainMenu/TopicCard.vue';
import Spinner from '../Spinner.vue';

const topicStore = useTopicStore();

onMounted(() => {
  topicStore.fetchTopics();
});
</script>

<template>
  <Spinner v-if="topicStore.loading" class="pt-48" />

  <div class="flex justify-center py-20 md:pt-40">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-x-20 gap-y-10">
      <TopicCard 
        v-for="(topic, index) in topicStore.topics" 
        :key="index" 
        :topic="topic.name" 
        :id="Number(topic.id)"
      />
    </div>
  </div>
</template>
