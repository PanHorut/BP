<script setup>
  import { ref } from 'vue';
  import { useAuthStore } from '@/stores/useAuthStore';
  import { useRouter } from 'vue-router';

  // State Management
  const username = ref('');
  const passphrasePart1 = ref('');
  const passphrasePart2 = ref('');
  const passphrasePart3 = ref('');
  const usernameError = ref('');
  const passphraseError = ref('');

  // Accessing the Auth Store
  const authStore = useAuthStore();
  const router = useRouter();


  // Handle Form Submission
  const handleLogin = async () => {
    // Reset Errors
    usernameError.value = '';
    passphraseError.value = '';
    authStore.errorMessage = '';

    // Construct the full passphrase
    const passphrase = `${passphrasePart1.value}-${passphrasePart2.value}-${passphrasePart3.value}`;

    // Validation
    if (username.value.trim() === '') {
      usernameError.value = 'Prosím, zadejte přezdívku.';
    }
    if (
      passphrasePart1.value.trim() === '' ||
      passphrasePart2.value.trim() === '' ||
      passphrasePart3.value.trim() === ''
    ) {
      passphraseError.value = 'Prosím, zadejte všechny části přístupového kódu.';
    }
    if (usernameError.value || passphraseError.value) {
      return;
    }

    // Use Auth Store to handle the login process
    await authStore.login(username.value, passphrase, router, true, false);
    
  };
</script>

<template>
  <div class="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-lg mt-12 mb-4 ">
    <h2 class="text-4xl font-bold text-primary mb-16 text-center">Přihlášení</h2>
    <form @submit.prevent="handleLogin">
      <!-- Username Field -->
      <div class="mb-4">
        <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Přezdívka</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          placeholder="Tvá přezdívka" 
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
        />
        <span class="text-red-600 ml-1">{{ usernameError ? usernameError : '' }}</span>
      </div>

      <!-- Passphrase Field (Split into 3 inputs) -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Přístupový kód</label>
        <div class="flex justify-between space-x-2">
          <input 
            type="text" 
            v-model="passphrasePart1" 
            maxlength="20"
            placeholder="část 1" 
            class="w-1/3 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-center" 
          />
          <span class="self-center text-gray-500">-</span>
          <input 
            type="text" 
            v-model="passphrasePart2" 
            maxlength="20"
            placeholder="část 2" 
            class="w-1/3 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-center" 
          />
          <span class="self-center text-gray-500">-</span>
          <input 
            type="text" 
            v-model="passphrasePart3" 
            maxlength="20"
            placeholder="část 3" 
            class="w-1/3 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-center" 
          />
        </div>
        <span class="text-red-600 ml-1">{{ passphraseError ? passphraseError : '' }}</span>
      </div>

      <!-- Error Message from Store -->
      <p v-if="authStore.errorMessage" class="bg-red-600 text-white w-full rounded-md font-medium text-lg text-center my-4">{{ authStore.errorMessage }}</p>

      <!-- Submit Button -->
      <button type="submit" 
              class="w-full py-2 bg-secondary text-white font-semibold rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
        Přihlásit se
      </button>
    </form>
  </div>
</template>
