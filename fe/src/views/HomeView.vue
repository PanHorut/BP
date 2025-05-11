<!--
================================================================================
 Component: HomeView.vue
 Description:
        Displays landing page for user and admin.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import Topics from '@/components/MainMenu/Topics.vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { onMounted } from 'vue';
import { useRoute} from 'vue-router';
import { useRecorderStore } from '@/stores/useRecorderStore';
import { useLanguageStore } from '@/stores/useLanguageStore';

// Stores
const authStore = useAuthStore();
const route = useRoute();
const langStore = useLanguageStore();
const recorderStore = useRecorderStore();

onMounted(() => {
  const lang = route.meta.lang;
  langStore.setLanguage(lang);
  
  // Set ASR language based on the selected language
  if(langStore.language === 'en') {
    recorderStore.changeASRLanguage('en-US');
  } else {
    recorderStore.changeASRLanguage('cs-CZ');
  }
});
</script>

<template>
  
  <!-- View for user - skills -->
  <Topics v-if="authStore.role != 'admin'"></Topics>
  
  <!-- View for admin - tasks and skills management -->
  <div v-else>
    <p class="text-4xl text-primary flex justify-center font-bold pt-16">
      Vítejte na hlavní stránce
    </p>

    <div class="flex flex-col items-center justify-center gap-8 pt-16">

      <!-- Task list and creator -->
      <RouterLink to="/tasks" class="w-96 cursor-pointer border border-gray-300 rounded-lg shadow-lg max-w-md bg-white 
           transition transform  hover:shadow-xl 
           hover:bg-secondary hover:border-secondary flex items-center justify-center text-3xl text-center font-bold text-primary p-4 
              duration-300 ease-in-out hover:text-white">
        Příklady
      </RouterLink>

      <!-- Skill list and creator -->
      <RouterLink to="/skill-creator" class="w-96 cursor-pointer border border-gray-300 rounded-lg shadow-lg max-w-md bg-white 
           transition transform  hover:shadow-xl 
           hover:bg-secondary hover:border-secondary flex items-center justify-center text-3xl text-center font-bold text-primary p-4 
              duration-300 ease-in-out hover:text-white"> 
        Dovednosti
      </RouterLink>
      
    </div>
    
  </div>

</template>
