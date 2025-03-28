<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import generatePassphrase from '@/utils/passphraseGenerator';  
import { registerStudent } from '@/api/apiClient';
import { useAuthStore } from '@/stores/useAuthStore';

// State Management
const username = ref('');
const passphrase = ref('');
const usernameError = ref('');
const passphraseError = ref('');
const showPassphrase = ref(false);
const copied = ref(false);
const errorMessage = ref('');

// Store & Router
const authStore = useAuthStore();
const router = useRouter();

// Function to handle form submission
const handleSubmit = async () => {
  // Reset Errors
  usernameError.value = '';
  passphraseError.value = '';
  errorMessage.value = '';

  // Form Validation
  if(username.value.trim() === '' || passphrase.value.trim() === ''){
    if (username.value.trim() === '') {
      usernameError.value = 'Zapomněl jsi vyplnit přezdívku';
    }
    if (passphrase.value.trim() === '') {
      passphraseError.value = 'Nejprve si musíš vygenerovat přístupový kód';
    }
    return;
  } 

  // API Call
  const result = await registerStudent(username.value, passphrase.value);

  // Handle Registration Response
  if (result.status === 201) {  // Assuming 201 Created for successful registration
    // Auto-Login after successful registration
    await authStore.login(username.value, passphrase.value, router, false, false);

    // Redirect to a protected route or home page
  } else {
    usernameError.value = result.error;
  }
};


// Function to generate a passphrase using random-words
const getPassphrase = () => {
  try {
    passphrase.value = generatePassphrase();
    showPassphrase.value = true;
    copied.value = false; 
    
  } catch (error) {
    console.error("Passphrase generation error:", error); 
  }
};

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
    <h2 class="text-4xl font-bold text-primary mb-16 text-center">Registrace</h2>
    <form @submit.prevent="handleSubmit">
      <div class="mb-4">
        <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Přezdívka</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          placeholder="Tvá přezdívka" 
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
        />
        <span class="text-red-600 ml-1">{{ usernameError }}</span>
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Přístupový kód</label>
        <div 
          class="w-full text-gray-700 font-bold text-center flex items-center justify-between space-x-2 h-6 text-lg">
          <div></div>
          <span :class="[passphrase ? '' : 'text-gray-500']">{{ passphrase ? passphrase : 'Vygeneruj si svůj přístupový kód'}}</span>
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
          Zkopírováno!
        </span>
        <span class="text-red-600 flex">{{ passphraseError }}</span>
      </div>

      <div class="mb-4 text-center">
        <button 
          type="button" 
          @click="getPassphrase"
          class="w-4/6 py-2 bg-green-500 text-white font-semibold rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500">
          Vygenerovat kód
        </button>
      </div>
      
      <button type="submit" 
              class="w-full py-2 bg-secondary text-white font-semibold rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
        Registrovat se
      </button>
    </form>

    <p v-if="errorMessage" class="text-red-600 text-sm text-center mt-4">{{ errorMessage }}</p>
  </div>
</template>

