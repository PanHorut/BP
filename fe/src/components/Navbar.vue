<script setup>
import { RouterLink, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/useAuthStore';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLanguageStore } from '@/stores/useLanguageStore';
import { useRecorderStore } from '@/stores/useRecorderStore';
import { dictionary } from '@/utils/dictionary';

// Auth Store
const authStore = useAuthStore();
const router = useRouter();
const langStore = useLanguageStore();
const recorderStore = useRecorderStore();

// Computed Property for Auth State
const isAuthenticated = computed(() => authStore.isAuthenticated);

// Mobile Menu State
const isMenuOpen = ref(false);

const changeLanguage = () => {
  langStore.setLanguage();
  if(langStore.language === 'en') {
    recorderStore.changeASRLanguage('en-US');
  } else {
    recorderStore.changeASRLanguage('cs-CZ');
  }
};
</script>

<template>
  <nav class="bg-primary shadow relative z-50">
    <div class="px-4 sm:px-6 lg:px-9">
      <div class="flex h-20 items-center justify-between">
        <!-- Left: Logo (Switches on small screens) -->
        <div class="flex items-center">
          <RouterLink to="/">
            <!-- Logo: Icon for mobile, text for md+ -->
            <img src="/app.ico" alt="App Logo" class="w-14 h-14 md:hidden" />
            <h1 class="text-4xl font-black tracking-wide text-white hidden md:block">{{ dictionary[langStore.language].logo }}</h1>
          </RouterLink>
        </div>

        <!-- Mobile Menu Button -->
        <button @click="isMenuOpen = !isMenuOpen"
          class="md:hidden text-white text-5xl focus:outline-none transition-transform duration-300"
          :class="isMenuOpen ? 'rotate-180' : 'rotate-0'">
          <i class="fa-solid transition-transform duration-300" 
            :class="isMenuOpen ? 'fa-times scale-110' : 'fa-bars scale-100'"></i>
        </button>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center space-x-8 text-2xl font-semibold">
          <template v-if="!isAuthenticated">
            <RouterLink to="/profile" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">{{dictionary[langStore.language].login}}</RouterLink>
            <button @click="changeLanguage">{{langStore.language == 'cs' ? '🇬🇧' : '🇨🇿' }}</button>
          </template>

          <template v-else-if="authStore.role == 'admin'">
            <RouterLink to="/tasks" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Příklady</RouterLink>
            <RouterLink to="/skill-creator" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Dovednosti</RouterLink>
            <button @click="authStore.logout(router)" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">Odhlásit se</button> 
            
          </template>

          <template v-else>
            <RouterLink to="/profile" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">{{dictionary[langStore.language].profile}}</RouterLink>
            <button @click="authStore.logout(router)" class="text-white hover:text-gray-200 border-b-2 border-primary hover:border-white transition">{{dictionary[langStore.language].logout}}</button>
            <button @click="changeLanguage">{{langStore.language == 'cs' ? '🇬🇧' : '🇨🇿' }}</button>

          </template>
        </div>
      </div>

      <!-- Mobile Menu (Dropdown) -->
      <transition name="fade">
        <div v-if="isMenuOpen" class="md:hidden flex flex-col items-center bg-primary text-white py-4 space-y-4 text-xl">
          <template v-if="!isAuthenticated">
            <RouterLink to="/profile" class="text-white text-3xl font-semibold" @click="isMenuOpen = false">{{dictionary[langStore.language].login}}</RouterLink>
            <button @click="changeLanguage">{{langStore.language == 'cs' ? '🇬🇧' : '🇨🇿' }}</button>

          </template>

          <template v-else-if="authStore.role == 'admin'">
            <RouterLink to="/tasks" class="text-white text-3xl font-semibold" @click="isMenuOpen = false">Příklady</RouterLink>
            <RouterLink to="/skill-creator" class="text-white text-3xl font-semibold" @click="isMenuOpen = false">Dovednosti</RouterLink>
            <button @click="authStore.logout(router); isMenuOpen = false" class="text-white text-3xl font-semibold">Odhlásit se</button> 
          </template>

          <template v-else>
            <RouterLink to="/profile" class="text-white text-3xl font-semibold" @click="isMenuOpen = false">{{dictionary[langStore.language].profile}}</RouterLink>
            <button @click="authStore.logout(router); isMenuOpen = false" class="text-white text-3xl font-semibold">{{dictionary[langStore.language].logout}}</button>
            <button @click="changeLanguage">{{langStore.language == 'cs' ? '🇬🇧' : '🇨🇿' }}</button>

          </template>
        </div>
      </transition>
    </div>
  </nav>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
