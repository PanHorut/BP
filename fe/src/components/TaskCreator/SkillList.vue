<script setup>
import { ref, defineEmits, defineExpose, nextTick } from 'vue';
import { searchSkills } from '@/api/apiClient';

// State for storing selected skills
const selectedSkills = ref([]);
const emits = defineEmits(['update-skills']);

// Autocomplete states
const query = ref('');
const suggestions = ref([]);
const inputRef = ref(null);

// Fetch skills from backend
const fetchSkills = async () => {
  if (query.value.length < 2) {
    suggestions.value = [];
    return;
  }
  try {
    suggestions.value = await searchSkills(query.value) || [];
  } catch (error) {
    console.error("Error fetching skills:", error);
    suggestions.value = [];
  }
};

// Function to add a skill from suggestions
const selectSkill = (skill) => {
  if (!selectedSkills.value.some(s => s.id === skill.id)) {
    selectedSkills.value.push(skill);
    emits('update-skills', selectedSkills.value);
  }
  query.value = ''; // Clear input
  suggestions.value = []; // Hide suggestions
  
  nextTick(() => {
    inputRef.value?.focus(); // Keep input field focused
  });
};

// Function to remove a skill
const removeSkill = (skill) => {
  selectedSkills.value = selectedSkills.value.filter((s) => s.id !== skill.id);
  emits('update-skills', selectedSkills.value);
};

// Import & clear skills functions
const importSkills = (skills) => {
  selectedSkills.value = skills;
};

const clearSkills = () => {
  selectedSkills.value = [];
};

defineExpose({ importSkills, clearSkills });
</script>

<template>
  <div class="flex flex-col items-start w-full">
    <h1 class="text-primary font-bold text-2xl mb-2">Schopnosti</h1>
    
    <div class="relative w-full max-w-4xl">
      <div class="border border-tertiary rounded p-2 flex flex-wrap min-h-12">
        <!-- Selected Skills -->
        <div v-for="(skill, index) in selectedSkills" :key="index" 
             class="flex items-center bg-tertiary px-2 py-1 m-1 rounded-xl">
          <span class="text-gray-600 font-bold">{{ skill.name }}</span>
          <button @click="removeSkill(skill)" class="ml-2 text-red-500 font-bold">&times;</button>
        </div>
        
        <!-- Input Field -->
        <input ref="inputRef" type="text" v-model="query" @input="fetchSkills" placeholder="Enter skill..."
               class="border-none outline-none flex-grow p-1" />
      </div>
      
      <!-- Suggestions -->
      <ul v-if="suggestions.length" class="absolute w-full border bg-white mt-1 rounded shadow">
        <li v-for="skill in suggestions" :key="skill.id" @click="selectSkill(skill)"
            class="p-2 hover:bg-gray-200 cursor-pointer">
          {{ skill.name }}
        </li>
      </ul>
    </div>
  </div>
</template>
