<script setup>
import { ref, onMounted } from 'vue';
import { getSkillTree } from '@/api/apiClient'; 
import SkillNode from '@/components/SkillCreator/SkillNode.vue';

const skillTree = ref([]); 

onMounted(async () => {
  try {
    skillTree.value = await getSkillTree(); 
  } catch (error) {
    console.error('Error fetching parent skills:', error);
  }
});
</script>

<template>
  <div class="flex flex-col w-full max-w-4xl mx-auto pt-12">
    <h2 class="text-4xl font-bold text-primary my-4 text-center">Dovednosti</h2>

    <SkillNode v-if="skillTree.length" :skills="skillTree" :parent="0" />
  </div>
</template>

