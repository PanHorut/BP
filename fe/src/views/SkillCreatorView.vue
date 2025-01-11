<script setup>
import { ref, onMounted } from 'vue';
import { getParentSkills, createSkill } from '@/api/apiClient'; 
import ToastManager from '@/components/Toast/ToastManager.vue';

const skillName = ref(''); 
const parentSkillId = ref(null); 
const parentSkills = ref([]); 

const toastManager = ref(null);

onMounted(async () => {
  try {
    parentSkills.value = await getParentSkills(); 
  } catch (error) {
    console.error('Error fetching parent skills:', error);
  }
});

const addSkill = async () => {
  if (!skillName.value.trim()) {
    toastManager.value.showToast('Nebyl zadán název dovednosti!', 'error');

    return;
  }

  try {
    const newSkill = await createSkill(skillName.value, parentSkillId.value);

    toastManager.value.showToast('Dovednost byla vytvořena', 'success');
    skillName.value = ''; 
    parentSkillId.value = null;
  } catch (error) {
    toastManager.value.showToast('Chyba!', 'error');
  }
};
</script>

<template>
    <ToastManager ref="toastManager" />

  <div class="p-4 max-w-md mx-auto bg-white rounded-lg shadow-md mt-64">

    <!-- Input for the new skill name -->
    <div class="mb-4">
      <label for="skillName" class="block text-sm font-medium text-gray-700 mb-1">Název nové dovednosti</label>
      <input
        id="skillName"
        v-model="skillName"
        type="text"
        class="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        placeholder="Zadejte název dovednosti"
      />
    </div>

    <!-- Dropdown for selecting parent skill -->
    <div class="mb-4">
      <label for="parentSkill" class="block text-sm font-medium text-gray-700 mb-1">Nadřazená dovednost</label>
      <select
        id="parentSkill"
        v-model="parentSkillId"
        class="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="" disabled>Vyberte nadřazenou dovednost</option>
        <option v-for="skill in parentSkills" :key="skill.id" :value="skill.id">
          {{ skill.name }}
        </option>
      </select>
    </div>

    <!-- Button to add the new skill -->
    <div class="flex justify-center">
      <button
        @click="addSkill"
        class="bg-green-500 text-white font-bold px-4 py-2 rounded-md shadow hover:bg-green-700"
      >
        Vytvořit dovednost
      </button>
    </div>
  </div>
</template>
