<script setup>
import { ref } from 'vue';
import { createSkill } from '@/api/apiClient'; 

const props = defineProps({
  skills: Array,
  parent: Number
});

const expanded = ref({});
const newSkillName = ref({});
const isAdding = ref(false);
const isAddingChild = ref({});
const skills = ref(props.skills);

const toggleExpand = (id) => {
  expanded.value[id] = !expanded.value[id];
};

const startAdding = () => {
  isAdding.value = true;
};

const startAddingChild = (skillId) => {
  isAddingChild.value[skillId] = true;
};

const addSkill = async (parentSkill, isChild = false) => {
  if (!newSkillName.value[parentSkill] || !newSkillName.value[parentSkill].trim()) return;

  try {
    const newSkill = await createSkill(newSkillName.value[parentSkill], parentSkill || null);
    newSkill.children = [];

    if (isChild && parentSkill) {

      // Find parent and add child directly
      const parentIndex = skills.value.findIndex(skill => skill.id === parentSkill);
      if (parentIndex !== -1) {
        if (!skills.value[parentIndex].children) {
          skills.value[parentIndex].children = [];
        }
        skills.value[parentIndex].children.push(newSkill);
      }
    } else {
      // Add as a new skill (sibling)
      skills.value.push(newSkill);
    }

    // Ensure Vue tracks new skill properties
    expanded.value[newSkill.id] = false;
    isAddingChild.value[newSkill.id] = false;

    newSkillName.value[parentSkill] = ''; // Clear input field only for the relevant skill
    isAdding.value = false;
    if (parentSkill) isAddingChild.value[parentSkill] = false; // Hide input field

  } catch (error) {
    console.error('Error creating skill:', error);
  }
};




</script>

<template>
    <ul class="pl-4">
      <li v-for="skill in skills" :key="skill.id" class="mb-2">
        <div class="flex items-center justify-start bg-gray-100 p-2 rounded-lg shadow-sm">
          <!-- Expand/Collapse Button & Skill Name -->
          <div 
            @click="toggleExpand(skill.id)" 
            class="flex items-center gap-3 cursor-pointer hover:text-blue-500"
          >
            <span v-if="skill.children && skill.children.length" class="text-sm">
              <!-- Font Awesome Icons for Expanding/Collapsing -->
              <i 
                v-if="expanded[skill.id]" 
                class="fas fa-chevron-down text-gray-600"
              ></i>
              <i 
                v-else 
                class="fas fa-chevron-right text-gray-600"
              ></i>
            </span>
            <span class="font-medium text-gray-800">{{ skill.name }}</span>
          </div>
  
          <!-- Add Child Button -->
          <button 
            v-if="skill.children && skill.children.length === 0 && !isAddingChild[skill.id]" 
            @click="startAddingChild(skill.id)" 
            class="flex items-center justify-center w-8 h-8 ml-2 rounded-full bg-blue-500 text-white font-bold text-xl hover:bg-blue-600 shadow-md transition"
          >
            +    
   </button>
        </div>
  
        <!-- Child Input Field -->
        <div v-if="isAddingChild[skill.id]" class="flex items-center gap-2 ml-6 mt-2">
          <input 
            v-model="newSkillName[skill.id]" 
            @keyup.enter="addSkill(skill.id, true)" 
            placeholder="Název nové dovednosti"
            class="border border-gray-300 rounded-lg px-3 py-1 text-sm w-1/3 focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
          <button @click="addSkill(skill.id, true)" class="px-3 py-1 text-white bg-green-500 rounded-lg hover:bg-green-600 transition"><i class="fa-solid fa-check"></i></button>
          <button @click="isAddingChild[skill.id] = false" class="px-3 py-1 text-white bg-red-500 rounded-lg hover:bg-red-600 transition"><i class="fa-solid fa-xmark"></i></button>
        </div>
  
        <!-- Show Children -->
        <SkillNode 
          v-if="expanded[skill.id] && skill.children && skill.children.length" 
          :skills="skill.children" 
          :parent="skill.id" 
          class="ml-6 border-l-2 border-gray-300 pl-4 mt-2"
        />
      </li>
  
      <!-- Show input when adding a new skill -->
      <li v-if="isAdding" class="flex items-center gap-2 mt-3">
        <input 
          v-model="newSkillName[props.parent]" 
          @keyup.enter="addSkill(props.parent, false)" 
          placeholder="Název nové dovednosti"
          class="border border-gray-300 rounded-lg px-3 py-1 text-sm w-1/3 focus:outline-none focus:ring-2 focus:ring-blue-300"
        />
        <button @click="addSkill(props.parent, false)" class="px-3 py-1 text-white bg-green-500 rounded-lg hover:bg-green-600 transition"><i class="fa-solid fa-check"></i></button>
        <button @click="isAdding = false" class="px-3 py-1 text-white bg-red-500 rounded-lg hover:bg-red-600 transition"><i class="fa-solid fa-xmark"></i></button>
      </li>
  
      <!-- "+" Button to Add a New Skill -->
      <li v-if="!isAdding" class="mt-3 -ml-8">
        <button 
        v-if="!isAdding"    
        @click="startAdding"
        class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 text-white font-bold text-xl hover:bg-blue-600 shadow-md transition"
    >
        +
    </button>
      </li>
    </ul>
    

  </template>
  