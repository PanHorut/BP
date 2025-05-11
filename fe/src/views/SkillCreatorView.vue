<!--
================================================================================
 Component: SkillCreatorView.vue
 Description:
      Displays the skill tree with functionality to create and delete skills.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, onMounted } from 'vue';
import { getSkillTree, getRelatedTasksCount ,deleteSkill } from '@/api/apiClient'; 
import SkillNode from '@/components/SkillCreator/SkillNode.vue';
import { useToastStore } from '@/stores/useToastStore';
import Spinner from '@/components/Spinner.vue';

const skillTree = ref([]); 
const loading = ref(true);
const deletedSkillName = ref('');
const deletedSkillId = ref('');

// Modal window variables
const isModalOpened = ref(false);
const relatedTasks = ref(0);
const relatedExamples = ref(0);

const toastStore = useToastStore();

// Fetch the skill tree
onMounted(async () => {
  try {
    skillTree.value = await getSkillTree(); 
  } catch (error) {
    console.error('Error fetching parent skills:', error);
  } finally{
    loading.value = false;
  }
});
 
// Open modal when admin wants to delete a skill
const openModal = async (name, id) => {
  const data = await getRelatedTasksCount(id);

  deletedSkillName.value = name;
  deletedSkillId.value = id;
  relatedTasks.value = data.task_count;
  relatedExamples.value = data.example_count;    
  isModalOpened.value = true;

};

// Cancel delete
const closeModal = () => {
  isModalOpened.value = false;
  deletedSkillName.value = '';
  deletedSkillId.value = '';
  relatedTasks.value = 0; 
  relatedExamples.value = 0;
};

// Confirm deletion of the skill and update the skill tree
const confirmDelete = async () => {
  try {
    await deleteSkill(deletedSkillId.value);
    
    const removeSkillFromTree = (skills) => {
      const index = skills.findIndex(skill => skill.id === deletedSkillId.value);
      
      // If found, remove it from the array
      if (index !== -1) {
        skills.splice(index, 1);
        return true;
      }

      // If not found, check in its children
      for (let i = 0; i < skills.length; i++) {
        if (skills[i].children && skills[i].children.length) {
          if (removeSkillFromTree(skills[i].children)) {
            return true;
          }
        }
      }
      return false; 
    };
    
    removeSkillFromTree(skillTree.value);
    
    toastStore.addToast({
      message: `Dovednost ${deletedSkillName.value} byla smazána`,
      type: 'success',
      visible: true,
    });
    
    closeModal();

  } catch (error) {
    toastStore.addToast({
      message: `Chyba při mazání dovednosti`,
      type: 'error',
      visible: true,
    });
  }
};

// Get correct form of word 'sada'
const getCorrectFormOfTask = (count) => {
  if (count === 1) {
    return 'sadou';
  } else  {
    return 'sadami';
  }
};

// Get correct form of word 'priklad'
const getCorrectFormOfExample = (count) => {
  if (count === 1) {
    return 'příkladem';
  } else  {
    return 'příklady';
  }
};
</script>

<template>

  <div class="flex flex-col w-full max-w-4xl mx-auto pt-12">
    <h2 class="text-4xl font-bold text-primary my-4 text-center">Dovednosti</h2>

    <!-- Skill tree root -->
    <SkillNode v-if="skillTree.length" :skills="skillTree" :parent="0" @deleteSkill="openModal"/>

    <Spinner v-if="loading" />
  </div>

  <!-- Delete skill confirmation modal -->
  <div v-if="isModalOpened" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-2/3 md:w-1/2">
      <p class="text-2xl">Opravdu chcete smazat dovednost <span class="font-bold">{{ deletedSkillName }}</span>?</p>
      <p class="mt-2 text-lg text-gray-600">Dovednost je spojena s {{ relatedTasks + ' ' + getCorrectFormOfTask() }} a {{ relatedExamples + ' ' + getCorrectFormOfExample()}}</p>
      <p class="mt-2 text-lg font-semibold text-red-600"><i class="fa-solid fa-triangle-exclamation text-xl"></i> Tato akce je nevratná </p>
      <div class="mt-4 flex justify-end gap-2 text-xl font-semibold">
        <button @click="closeModal" class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400">Zrušit</button>
        <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">Smazat</button>
      </div>
    </div>
  </div>

</template>

