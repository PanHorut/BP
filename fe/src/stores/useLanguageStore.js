import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useLanguageStore = defineStore('language', () => {
  const language = ref('cs');

  function setLanguage() {
    language.value = language.value === 'cs' ? 'en' : 'cs';
}

  return { language, setLanguage };
});