import { defineStore } from 'pinia';

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [],
  }),
  actions: {
    addToast(toast) {
        this.toasts.push(toast);
        setTimeout(() => {
          this.removeToast(this.toasts.indexOf(toast)); // Remove toast after 3 seconds
        }, 3000);
      },
      
    removeToast(index) {
      this.toasts.splice(index, 1);
    },
  },
});
