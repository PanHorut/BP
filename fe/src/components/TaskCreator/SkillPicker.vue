<script setup>
import { ref, defineEmits, defineProps, watch, onMounted } from 'vue'; // Make sure to import watch
import axios from 'axios'
// Emit setup
const emit = defineEmits(['update:selectedItems']);

// Props
const props = defineProps({
  selectedItems: {
    type: Array,
    default: () => []
  }
});




const items = ref([])


// State variables
const isModalOpen = ref(false);
const selectedItems = ref(props.selectedItems); // Initialize with selectedItems prop

// Watch for changes in selectedItems prop
watch(() => props.selectedItems, (newVal) => {
  selectedItems.value = newVal;
});

// Methods
const clearSelection = () => {
  selectedItems.value = [];
  emit('update:selectedItems', selectedItems.value);
};

const applySelection = () => {
  isModalOpen.value = false;
  emit('update:selectedItems', selectedItems.value); // Emit selected items to parent
};

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/leaf-skills/') // Adjust the URL as needed
    items.value = response.data
  } catch (error) {
    console.error("Error fetching skills:", error)
  }
})
</script>

<template>
    
    <button @click="isModalOpen = true" class="w-10 h-10 bg-secondary text-white text-xl font-black rounded-lg">
      +
    </button>
  
    <div v-if="isModalOpen" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white rounded-lg shadow-lg w-10/12 p-5">
        
        <div class="flex justify-between items-center border-b pb-3">
          <div></div>  
          <h3 class="text-xl text-secondary font-semibold">Vyberte procvičené schopnosti</h3>
          <button @click="isModalOpen = false" class="text-gray-600 hover:text-gray-800 text-4xl">&times;</button>
        </div>
  
        
        <div class="mt-4 w-full">
            <ul class="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <li v-for="(item, index) in items" :key="index" class="flex items-center mb-2">
              <input
                type="checkbox"
                :id="`item-${index}`"
                v-model="selectedItems"
                :value="item"
                class="w-6 h-6 rounded-lg border-primary text-primary"
              />
              <label :for="`item-${index}`" class="ml-2 text-secondary text-lg whitespace-nowrap">{{ item.name }}</label>
            </li>
          </ul>
        </div>
  
        <!-- Modal Footer with Actions -->
        <div class="flex justify-end mt-5 space-x-3">
          <button @click="clearSelection" class="px-4 py-2 bg-gray-200 text-gray-800 rounded">
            Vybrat vše
          </button>
          <button @click="applySelection" class="px-4 py-2 bg-secondary text-white font-black rounded">
            Uložit
          </button>
        </div>
      </div>
    </div>
    
  </template>
  
 