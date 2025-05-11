/**
 * ================================================================================
 * File: useToastStore.js
 * Description:
 *       Pinia store for managing toast notifications in the application.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

import { defineStore } from 'pinia';

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [],
  }),
  actions: {
    // Add a toast notification to the list and remove it after 3 seconds
    addToast(toast) {
        this.toasts.push(toast);
        setTimeout(() => {
          this.removeToast(this.toasts.indexOf(toast)); 
        }, 3000);
      },
      
    // Remove a toast notification by its index  
    removeToast(index) {
      this.toasts.splice(index, 1);
    },
  },
});
