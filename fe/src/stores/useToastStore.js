import { defineStore } from 'pinia';

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [],
  }),
  actions: {
    addToast(toast) {
        this.toasts.push(toast);
        setTimeout(() => {
          this.removeToast(this.toasts.indexOf(toast)); 
        }, 3000);
      },
      
    removeToast(index) {
      this.toasts.splice(index, 1);
    },
  },
});
