<script setup>
import TopicCard from '@/components/TopicCard.vue';

</script>

<template>
    <div class="flex justify-center p-11">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-x-20 gap-y-10">
        <TopicCard topic="Zlomky"></TopicCard>
        <TopicCard topic="Desetinná čísla"></TopicCard>
        <TopicCard topic="Celá čísla"></TopicCard>
        <TopicCard topic="Lineární rovnice"></TopicCard>
        <TopicCard topic="Výrazy"></TopicCard>
        <TopicCard topic="Procenta"></TopicCard>
      </div>
    </div>
  </template>