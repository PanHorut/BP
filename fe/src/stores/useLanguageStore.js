/**
 * ================================================================================
 * File: useLanguageStore.js
 * Description:
 *       Pinia store for managing the applications language.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useLanguageStore = defineStore('language', () => {
  
  const language = ref('cs');

  function setLanguage(lang) {
    language.value = lang;
  }

  function toggleLanguage() {
    language.value = language.value === 'cs' ? 'en' : 'cs';
  }

  return {
    language,
    setLanguage,
    toggleLanguage
  };
});