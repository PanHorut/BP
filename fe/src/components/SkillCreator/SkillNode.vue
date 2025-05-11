<!--
================================================================================
 Component: SkilNode.vue
 Description:
        Displays node in skill tree structure recursively and allows to create and delete skills.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, nextTick } from 'vue';
import { createSkill } from '@/api/apiClient'; 
import { useToastStore } from '@/stores/useToastStore';

const props = defineProps({
  skills: Array,
  parent: Number
});

// Tracks expanded/collapsed skill nodes
const expanded = ref({});

// Tracks input values for new skill names
const newSkillName = ref({});

// Tracks if adding a sibling skill
const isAdding = ref(false);

// Tracks if adding a child skill
const isAddingChild = ref({});

const skills = ref(props.skills);

// Refs to input elements for focusing
const newSkillInput = ref(null);
const childSkillInputs = ref({});

const toastStore = useToastStore();

const emit = defineEmits(['deleteSkill']);

// Toggle skill node exapanded/collapsed
const toggleExpand = (id) => {
  expanded.value[id] = !expanded.value[id];
};

// Start adding at sibling skill level
const startAdding = async () => {
  isAdding.value = true;
  await nextTick();
  newSkillInput.value?.focus();
};

// Start adding at child skill level
const startAddingChild = async (skillId) => {
  isAddingChild.value[skillId] = true;
  await nextTick();
  childSkillInputs.value[skillId]?.focus();
};

const vFocus = {
  mounted: (el) => el.focus()
};

// Add new skill
const addSkill = async (parentSkill, isChild = false) => {
  if (!newSkillName.value[parentSkill] || !newSkillName.value[parentSkill].trim()) return;

  try {
    // Create new skill
    const newSkill = await createSkill(newSkillName.value[parentSkill], parentSkill || null);

    toastStore.addToast({
        message: `Dovednost ${newSkillName.value[parentSkill]} byla vytvořena`,
        type: 'success',
        visible: true,
    });

    newSkill.children = [];

    // Add to appropriate location
    if (isChild && parentSkill) {
      const parentIndex = skills.value.findIndex(skill => skill.id === parentSkill);
      if (parentIndex !== -1) {
        if (!skills.value[parentIndex].children) {
          skills.value[parentIndex].children = [];
        }
        skills.value[parentIndex].children.push(newSkill);
      }
    } else {
      skills.value.push(newSkill);
    }
    
    // Reset states
    expanded.value[newSkill.id] = false;
    isAddingChild.value[newSkill.id] = false;
    newSkillName.value[parentSkill] = ''; 
    isAdding.value = false;
    if (parentSkill) isAddingChild.value[parentSkill] = false;

  } catch (error) {
    console.error('Error creating skill:', error);
  }
};

// Emit sibling skill to delete to parent component
const removeSkill = async (name, id) => {
  emit('deleteSkill', name, id);  
  
};

// Emit child skill to delete to parent component
const removeChildSkill = (name, id) => {
  emit('deleteSkill', name, id);
};
</script>

<template>
  
  <ul class="pl-4">

    <li v-for="skill in skills" :key="skill.id" class="mb-2">

      <div class="flex items-center justify-start bg-gray-100 p-2 rounded-lg shadow-sm">

         <!-- Skill node -->
        <div @click="toggleExpand(skill.id)" class="flex items-center gap-3 cursor-pointer hover:text-blue-500">
          <span v-if="skill.children && skill.children.length" class="text-sm">
            <i v-if="expanded[skill.id]" class="fas fa-chevron-down text-gray-600"></i>
            <i v-else class="fas fa-chevron-right text-gray-600"></i>
          </span>
          <span class="font-medium text-gray-800">{{ skill.name }}</span>
        </div>

        
        <div class="flex">

          <!-- Show child creator -->
          <button v-if="skill.children && skill.children.length === 0 && !isAddingChild[skill.id]"
            @click="startAddingChild(skill.id)"
            class="flex items-center justify-center w-6 h-6 ml-2 rounded-full bg-blue-500 text-white font-bold text-sm hover:bg-blue-600 shadow-md transition">
            <i class="fa-solid fa-plus"></i>
          </button>

          <!-- Delete skill -->
          <button v-if="skill.children && skill.children.length === 0 && !isAddingChild[skill.id]"
            @click="removeSkill(skill.name, skill.id)"
            class="flex items-center justify-center w-6 h-6 ml-2 rounded-full bg-red-500 text-white font-bold text-sm hover:bg-red-600 shadow-md transition">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
      </div>

      <!-- Creating skill child -->
      <div v-if="isAddingChild[skill.id]" class="flex items-center gap-2 ml-6 mt-2">

        <!--New skill name -->
        <input v-model="newSkillName[skill.id]" ref="childSkillInputs" v-focus
          :ref="el => childSkillInputs.value[skill.id] = el" @keyup.enter="addSkill(skill.id, true)"
          placeholder="Název nové dovednosti"
          class="border border-gray-300 rounded-lg px-3 py-1 text-sm w-1/3 focus:outline-none focus:ring-2 focus:ring-blue-300" />

        <!-- Confirm creating skill -->
        <button @click="addSkill(skill.id, true)"
          class="px-3 py-1 text-white bg-green-500 rounded-lg hover:bg-green-600 transition">
          <i class="fa-solid fa-check"></i>
        </button>

        <!-- Cancel creating skill -->
        <button @click="isAddingChild[skill.id] = false"
          class="px-3 py-1 text-white bg-red-500 rounded-lg hover:bg-red-600 transition">
          <i class="fa-solid fa-xmark"></i>
        </button>
        
      </div>

      <!-- Child skills -->
      <SkillNode v-if="expanded[skill.id] && skill.children && skill.children.length" :skills="skill.children"
        :parent="skill.id" class="ml-6 border-l-2 border-gray-300 pl-4 mt-2" @deleteSkill="removeChildSkill" />

    </li>

    <!-- Creating sibling skill -->
    <li v-if="isAdding" class="flex items-center gap-2 mt-3">

      <!--New skill name -->
      <input v-model="newSkillName[props.parent]" ref="newSkillInput" @keyup.enter="addSkill(props.parent, false)"
        placeholder="Název nové dovednosti"
        class="border border-gray-300 rounded-lg px-3 py-1 text-sm w-1/3 focus:outline-none focus:ring-2 focus:ring-blue-300" />

      <!-- Confirm creating skill -->
      <button @click="addSkill(props.parent, false)"
        class="px-3 py-1 text-white bg-green-500 rounded-lg hover:bg-green-600 transition">
        <i class="fa-solid fa-check"></i>
      </button>

      <!-- Cancel creating skill -->
      <button @click="isAdding = false"
        class="px-3 py-1 text-white bg-red-500 rounded-lg hover:bg-red-600 transition">
        <i class="fa-solid fa-xmark"></i>
      </button>

    </li>

    <!-- Show sibling creator -->
    <li v-if="!isAdding && props.skills[0].parent_skill != null" class="mt-3 -ml-8">

      <button v-if="!isAdding" @click="startAdding"
        class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 text-white font-bold text-xl hover:bg-blue-600 shadow-md transition">
        <i class="fa-solid fa-plus"></i>
      </button>

    </li>

  </ul>
  
</template>
