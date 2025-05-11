<!--
================================================================================
 Component: Signup.vue
 Description:
        Displays user signup form.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import generatePassphrase from '@/utils/passphraseGenerator';  
import { registerStudent } from '@/api/apiClient';
import { useAuthStore } from '@/stores/useAuthStore';
import { dictionary } from '@/utils/dictionary';
import { useLanguageStore } from '@/stores/useLanguageStore';

const username = ref('');
const passphrase = ref('');

const usernameError = ref('');
const passphraseError = ref('');
const showPassphrase = ref(false);
const errorMessage = ref('');

const copied = ref(false);

const authStore = useAuthStore();
const router = useRouter();
const langStore = useLanguageStore();

// Handle signup form submission 
const handleSubmit = async () => {

  // Reset errors
  usernameError.value = '';
  passphraseError.value = '';
  errorMessage.value = '';

  // Validation 
  if(username.value.trim() === '' || passphrase.value.trim() === ''){

    if (username.value.trim() === '') {
      usernameError.value = dictionary[langStore.language].usernameForgot;
    }

    if (passphrase.value.trim() === '') {
      passphraseError.value = dictionary[langStore.language].passphraseForgot;
    }
    return;
  } 

  // Signup
  const result = await registerStudent(username.value, passphrase.value);
  
  // Successful signup -> login user with auth store
  if (result.status === 201) {  
    await authStore.login(username.value, passphrase.value, router, false, false);

  } else {
    usernameError.value = result.error;
  }
};

// Generate passphrase
const getPassphrase = () => {
  try {
    passphrase.value = generatePassphrase(langStore.language);
    showPassphrase.value = true;
    copied.value = false; 
    
  } catch (error) {
    console.error("Passphrase generation error:", error); 
  }
};

// Copy passphrase to clipboard
const copyToClipboard = () => {

  navigator.clipboard.writeText(passphrase.value)
    .then(() => {
      copied.value = true;
      setTimeout(() => {
        copied.value = false;
      }, 1500); 
    })
    .catch(err => {
      console.error('Failed to copy:', err);
    });
};
</script>


<template>
  <div class="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg mt-12 mb-4">

    <h2 class="text-4xl font-bold text-primary mb-16 text-center">{{dictionary[langStore.language].register}}</h2>

    <!-- Signup form -->
    <form @submit.prevent="handleSubmit">

      <!-- Username field -->
      <div class="mb-4">
        <label for="username" class="block text-sm font-medium text-gray-700 mb-2">{{dictionary[langStore.language].nickname}}</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          :placeholder="dictionary[langStore.language].nicknamePlaceholder" 
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
        />
        <span class="text-red-600 ml-1">{{ usernameError }}</span>
      </div>

      <!-- Passphrase -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">{{dictionary[langStore.language].accessCode}}</label>
        <div 
          class="w-full text-gray-700 font-bold text-center flex items-center justify-between space-x-2 h-6 text-lg">

          <div></div> <!--Placeholder used to center -->

          <!-- Generated passphrase -->
          <span :class="[passphrase ? '' : 'text-gray-500']">{{ passphrase ? passphrase : dictionary[langStore.language].generatePassphrasePlaceholder}}</span>

          <!-- Copy button -->
          <button 
            @click="copyToClipboard" 
            type="button"
            class="text-gray-500 hover:text-gray-700 focus:outline-none transition duration-200 ease-in-out transform hover:scale-110"
            :class="[showPassphrase ? 'visible' : 'invisible']">
            <i class="fa-solid fa-copy ml-2" style="color: #1d3557;"></i>
          </button>

        </div>

        <span
          class="text-primary text-sm text-center flex justify-center"
          :class="[copied ? 'visible' : 'invisible']">
          {{ dictionary[langStore.language].copied }}
        </span>

        <span class="text-red-600 flex">{{ passphraseError }}</span>

      </div>

      <div class="mb-4 text-center">
        <!-- Button to generate passphrase -->
        <button 
          type="button" 
          @click="getPassphrase"
          class="w-4/6 py-2 bg-green-500 text-white font-semibold rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500">
          {{ dictionary[langStore.language].generatePassphrase }}
        </button>
      </div>
      
      <!-- Submit Button -->
      <button type="submit" 
              class="w-full py-2 bg-secondary text-white font-semibold rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
        {{ dictionary[langStore.language].register }}
      </button>

    </form>

    <p v-if="errorMessage" class="text-red-600 text-sm text-center mt-4">{{ errorMessage }}</p>
    
  </div>
</template>

