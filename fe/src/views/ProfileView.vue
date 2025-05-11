<!--
================================================================================
 Component: ProfileView.vue
 Description:
        Displays user login or signup page.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import Signup from '@/components/Profile/Signup.vue';
import Login from '@/components/Profile/Login.vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { dictionary } from '@/utils/dictionary';
import { useLanguageStore } from '@/stores/useLanguageStore';
import { RouterLink } from 'vue-router';
import { ref } from 'vue';

const authStore = useAuthStore();
const langStore = useLanguageStore();
const showLogin = ref(true);

// Switch between login and signup
const toggleLogin = () => {
  showLogin.value = !showLogin.value;
};

</script>

<template>

  <!-- Placeholder if logged in -->
  <div v-if="authStore.isAuthenticated" class="w-full text-4xl text-primary flex flex-col items-center justify-center font-bold pt-12">
    <p>{{dictionary[langStore.language].hi}} {{ authStore.name }}!</p>
  </div>

  <div v-else class="pt-12">

    <Login v-if="showLogin" />
    <Signup v-else />

    <!-- Button to switch between login and signup -->
    <button @click="toggleLogin" class="underline w-full text-secondary text-lg">
      {{ showLogin ? dictionary[langStore.language].registerText : dictionary[langStore.language].loginText}}
    </button>

    <!-- Button to switch to admin login -->
    <RouterLink to="/admin" class="underline w-full text-secondary text-lg mt-12 flex justify-center">
      {{ dictionary[langStore.language].adminText }}
    </RouterLink>
    
  </div>

</template>

