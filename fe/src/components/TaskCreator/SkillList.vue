<script setup>
import { ref, defineEmits, defineExpose, nextTick, onMounted, onUnmounted } from 'vue';
import { searchSkills, getSandboxSkillPaths } from '@/api/apiClient';

// Store selected skill paths (each path is an array of skills)
const selectedSkillPaths = ref([]);
const selectedSkills = ref([]);


// Temporary skill selection for the current path
const currentSkillPath = ref([]);

const emits = defineEmits(['update-skills']);

// Autocomplete states
const query = ref('');
const suggestions = ref([]);
const inputRef = ref(null);
const componentRef = ref(null); // Reference to the entire component

// Fetch skills from backend
const fetchSkills = async () => {
  const mostRecentSkill = currentSkillPath.value[currentSkillPath.value.length - 1];

  let id = 54; // id of root skill
  if (mostRecentSkill) id = mostRecentSkill.id;

  try {
    suggestions.value = await searchSkills(query.value, id);
  } catch (error) {
    console.error("Error fetching skills:", error);
    suggestions.value = [];
  }
};

// Add a skill to the current path
const selectSkill = (skill) => {
  if (!currentSkillPath.value.some(s => s.id === skill.id)) {
    currentSkillPath.value.push(skill);

  }
  query.value = '';
  suggestions.value = [];
  fetchSkills();
  
  nextTick(() => {
    inputRef.value?.focus();
  });
};

// Remove only the last skill from the current path
const removeLastSkill = () => {
  currentSkillPath.value.pop();
};

// Confirm the current skill path and start a new one
const confirmSkillPath = () => {
  if (currentSkillPath.value.length) {
    selectedSkillPaths.value.push([...currentSkillPath.value]); // Save the path

    let allSkills = selectedSkillPaths.value.flat();

    // Remove duplicates based on skill ID
    selectedSkills.value = allSkills.filter((skill, index, self) => 
      index === self.findIndex((s) => s.id === skill.id)
    );

    emits('update-skills', selectedSkillPaths.value.flat());
    currentSkillPath.value = []; // Reset for new path
    query.value = '';
    fetchSkills(); // Fetch suggestions for new path
  }
};

// Handle Enter key press
const handleKeyDown = (event) => {
  if (event.key === 'Enter') {
    confirmSkillPath();
  }
};

// Handle focus and blur for suggestions visibility
const handleFocus = () => {
  fetchSkills();
};

// Handle clicks outside the component to clear suggestions
const handleClickOutside = (event) => {
  if (componentRef.value && !componentRef.value.contains(event.target)) {
    suggestions.value = [];
  }
};

// Listen for clicks outside the component
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

// Prevent blur event from clearing suggestions when clicking a suggestion
const handleSuggestionMouseDown = (event) => {
  event.preventDefault();
};

const removeSkill = (skill) => {
  selectedSkills.value = selectedSkills.value.filter((s) => s.id !== skill.id);
  emits('update-skills', selectedSkills.value);
};

const removeSkillPath = (pathIndex) => {
  selectedSkillPaths.value.splice(pathIndex, 1);
  emits('update-skills', selectedSkillPaths.value.flat()); // Update the parent component if needed
};


const importSkills = async (skills) => {
  console.log(skills);  
  const skillIds = skills.map(skill => skill.id);  // Extract only the IDs
  const paths = await getSandboxSkillPaths(skillIds); // Get paths as ID arrays

  // Convert paths (IDs) into paths of full skill objects
  selectedSkillPaths.value = paths.map(path => 
    path.map(skillId => skills.find(skill => skill.id === skillId))
  );

  selectedSkills.value = skills;
};


const clearSkills = () => {
  selectedSkills.value = [];
};

defineExpose({ importSkills, clearSkills });
</script>

<template>
  <div ref="componentRef" class="flex flex-col items-start w-full">
    <h1 class="text-primary font-bold text-2xl mb-2">Schopnosti</h1>

    <div class="relative w-full max-w-4xl">
      <div v-if="selectedSkillPaths.length" class="mb-2 p-2 border border-gray-300 rounded">
        <div v-for="(path, pathIndex) in selectedSkillPaths" :key="pathIndex"
          class="flex flex-wrap items-center relative">
          <template v-for="(skill, skillIndex) in path" :key="skillIndex">
            <span class="text-gray-700 bg-tertiary px-2 py-1 rounded-xl m-1">
              {{ skill.name }}
            </span>
            <i v-if="skillIndex !== path.length - 1" class="fa-solid fa-arrow-right mx-1 text-primary"></i>
          </template>

          <!-- Delete Button for the Path -->
          <button @click="removeSkillPath(pathIndex)"
            class="ml-2 bg-red-500 hover:bg-red-600 transition text-md font-bold w-8 h-8 rounded-lg">
            <i class="fa-solid fa-trash text-white"></i>
          </button>
        </div>
      </div>


      <div class="border border-tertiary rounded p-2 flex flex-wrap min-h-12 relative">
        <!-- Selected Skills for Current Path -->
        <div v-for="(skill, index) in currentSkillPath" :key="index"
          class="flex items-center bg-tertiary px-2 py-1 m-1 rounded-xl">
          <span class="text-gray-600 font-bold">{{ skill.name }}</span>
          <button v-if="index === currentSkillPath.length - 1" @click="removeLastSkill"
            class="ml-2 text-red-500 font-bold">
            &times;
          </button>
        </div>

        <!-- Input Field -->
        <input ref="inputRef" type="text" v-model="query" @input="fetchSkills" @focus="handleFocus"
          @keydown="handleKeyDown" placeholder="Vložte dovednost..."
          class="border-none outline-none focus:ring-0 focus:border-transparent bg-transparent flex-grow p-1 min-w-[150px]" />

        <button v-if="currentSkillPath.length" @click="confirmSkillPath"
          class=" bg-green-500 hover:bg-green-600 transition text-white w-10 h-10 rounded">
          <i class="fa-solid fa-check text-xl"></i>
        </button>
      </div>

      <!-- Suggestions (now matches the width of input field) -->
      <ul v-if="suggestions.length" class="absolute left-0 mt-1 border bg-white rounded shadow"
        :style="{ width: inputRef?.offsetWidth + 'px' }">
        <li v-for="skill in suggestions" :key="skill.id" @click="selectSkill(skill)"
          @mousedown="handleSuggestionMouseDown" class="p-2 hover:bg-gray-200 cursor-pointer">
          {{ skill.name }}
        </li>
      </ul>
    </div>

    <!-- Confirm Path Button -->

  </div>
</template>
