<script setup>
import { ref, defineEmits, defineExpose } from 'vue';
import SkillPicker from './SkillPicker.vue';

// State for storing selected items
const selectedSkills = ref([]);
const emits = defineEmits(['update-skills']);

// Function to update the selected skills
const updateSkills = (skills) => {
  selectedSkills.value = skills;
  emits('update-skills', selectedSkills.value); 
};

// Function to remove a skill
const removeSkill = (skill) => {
  // Remove from the selectedSkills array
  selectedSkills.value = selectedSkills.value.filter((s) => s !== skill);
};

const importSkills = (skills) => {
  selectedSkills.value = skills;
}

defineExpose({ importSkills });

</script>

<template>
  <div class="flex items-start justify-start w-full">
    
    <h1 class="text-primary font-bold text-2xl mr-1 max-w-32">Procvičené schopnosti</h1>

    <!-- Listen for update:selectedItems event -->
    <SkillPicker 
      :selectedItems="selectedSkills" 
      @update:selectedItems="updateSkills" 
    />

    <!-- Display selected items in a list -->
     <div class="ml-2 min-w-80 min-h-20 border border-tertiary ">
    <ul class="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 ">
      <li 
        v-for="(skill, index) in selectedSkills" 
        :key="index" 
        class="flex items-center justify-start bg-tertiary p-1 m-2 rounded-xl max-h-8"
      >
        <button 
          @click="removeSkill(skill)" 
          class="w-6 h-6 text-primary text-center font-bold rounded-md"
        >
          x
        </button>
        <span class="text-gray-600 font-bold px-1 whitespace-nowrap">{{ skill.name }}</span>
        
      </li>
    </ul>
    </div>
  </div>
</template>
