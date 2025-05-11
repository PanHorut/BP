/**
 * ================================================================================
 * File: useAuthStore.js
 * Description:
 *       Pinia store for managing authentication state, login/logout actions, and session handling.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */


import { defineStore } from 'pinia';
import { loginStudent, loginAdmin } from '@/api/apiClient';
import { useToastStore } from '@/stores/useToastStore';
import { dictionary } from '@/utils/dictionary';
import { useLanguageStore } from './useLanguageStore';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    id: null,
    role: null,
    isAuthenticated: false,
    errorMessage: '',
    inactivityTimeout: null,

  }),
  actions: {
    async login(username, passphrase, router, isLogin, isAdmin) {
      try {
        let result = null;

        
        if(isAdmin){
          // Admin tries to login
          result = await loginAdmin(username, passphrase);
        } else{
          // User tries to login
          result = await loginStudent(username, passphrase);
        }
        
        // Successful login
        if (result.status === 200) {
         
          // Save data in the store
          this.name = username;
          this.id = result.data.id;
          this.role = result.data.role;
          this.isAuthenticated = true;

          localStorage.setItem('name', JSON.stringify(this.name));
          localStorage.setItem('id', JSON.stringify(this.id));
          localStorage.setItem('role', JSON.stringify(this.role));

          this.startInactivityTimer(router);

          const langStore = useLanguageStore();
          const toastStore = useToastStore();

          toastStore.addToast({
            message: isLogin ? dictionary[langStore.language].loginSuccess : dictionary[langStore.language].registrationSuccess, 
            type: 'success',
            visible: true,
          });
          
          router.push({ name: 'home' });
        
        // Unsuccessful login
        } else {
          this.errorMessage = langStore.language == 'cs' ? result.error : dictionary[langStore.language].invalidCredentials;
        }
      } catch (error) {
        this.errorMessage = dictionary[langStore.language].somethingWentWrong;
      }
    },

    logout(router) {

      // Clear store data
      this.user = null;
      this.id = null;
      this.isAuthenticated = false;

      localStorage.removeItem('name');
      localStorage.removeItem('id');
      localStorage.removeItem('role');

      this.clearInactivityTimer();

      const toastStore = useToastStore();
      const langStore = useLanguageStore();

      toastStore.addToast({
        message: dictionary[langStore.language].logoutSuccess,
        type: 'info',
        visible: true,
      });

      // Redirect to home page and reload
      router.push({ name: 'home' }).then(() => {
        window.location.reload();
      });
    },

    // Load stored session data from localStorage
    loadStoredSession() {

      const storedName = localStorage.getItem('name');
      const storedId = localStorage.getItem('id');
      const storedRole = localStorage.getItem('role');

      if (storedName && storedId && storedRole) {
        this.name = JSON.parse(storedName);
        this.id = storedId;
        this.role = JSON.parse(storedRole);
        this.isAuthenticated = true;
      }
    },

    startInactivityTimer(router) {

      if (this.inactivityTimeout) {
        clearTimeout(this.inactivityTimeout);
      }
      
      // Log out user after 10 minutes of inactivity
      this.inactivityTimeout = setTimeout(() => {
        this.logout(router);
        
        const toastStore = useToastStore();
        const langStore = useLanguageStore();
        toastStore.addToast({
          message: dictionary[langStore.language].inactivityLogout, 
          type: 'info',
          visible: true,
        });
      }, 600000); // 10 minutes
    },
  
    // Reset the inactivity timer on user activity
    resetInactivityTimer(router) {
      this.startInactivityTimer(router);
    },
    
    // Clear the inactivity timer 
    clearInactivityTimer() {
      if (this.inactivityTimeout) {
        clearTimeout(this.inactivityTimeout);
        this.inactivityTimeout = null;
      }
    },
  },
});
