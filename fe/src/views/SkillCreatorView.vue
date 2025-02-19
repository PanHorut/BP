<script setup>
import { ref, onMounted } from 'vue';
import { getSkillTree } from '@/api/apiClient'; 
import SkillNode from '@/components/SkillCreator/SkillNode.vue';
import Spinner from '@/components/Spinner.vue';

const skillTree = ref([]); 
const loading = ref(true);

onMounted(async () => {
  try {
    skillTree.value = await getSkillTree(); 
  } catch (error) {
    console.error('Error fetching parent skills:', error);
  } finally{
    loading.value = false;
  }
});
</script>

<template>
  <div class="flex flex-col w-full max-w-4xl mx-auto pt-12">
    <h2 class="text-4xl font-bold text-primary my-4 text-center">Dovednosti</h2>

    <SkillNode v-if="skillTree.length" :skills="skillTree" :parent="0" />
    <Spinner v-if="loading" />

  </div>
</template>

