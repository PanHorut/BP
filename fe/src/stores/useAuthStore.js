import { defineStore } from 'pinia';
import { loginStudent, loginAdmin } from '@/api/apiClient';
import { useToastStore } from '@/stores/useToastStore';

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
          result = await loginAdmin(username, passphrase);
        } else{
          result = await loginStudent(username, passphrase);
        }
        
        if (result.status === 200) {
          // Store user info and token
          this.name = username;
          this.id = result.data.id;
          this.role = result.data.role;
          this.isAuthenticated = true;

          localStorage.setItem('name', JSON.stringify(this.name));
          localStorage.setItem('id', JSON.stringify(this.id));
          localStorage.setItem('role', JSON.stringify(this.role));

          this.startInactivityTimer(router);

          const toastStore = useToastStore();
          toastStore.addToast({
            message: isLogin ? 'Přihlášení proběhlo úspěšně' : 'Registrace proběhla úspěšně', 
            type: 'success',
            visible: true,
          });
          

          // Redirect to a protected route
          if(isAdmin){
            router.push({ name: 'admin' });

          }else{
            router.push({ name: 'home' });
          }

        } else {
          this.errorMessage = result.error;
        }
      } catch (error) {
        this.errorMessage = 'Něco se pokazilo. Zkuste to znovu později.';
      }
    },
    logout(router) {
      this.user = null;
      this.id = null;
      this.isAuthenticated = false;

      localStorage.removeItem('name');
      localStorage.removeItem('id');
      localStorage.removeItem('role');

      this.clearInactivityTimer();


      const toastStore = useToastStore();
      toastStore.addToast({
        message: 'Odhlášení proběhlo úspěšně',
        type: 'info',
        visible: true,
      });

      router.push({ name: 'home' });
    },
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
  
      this.inactivityTimeout = setTimeout(() => {
        this.logout(router);
        
        const toastStore = useToastStore();
        toastStore.addToast({
          message: 'Byli jste odhlášeni z důvodu neaktivity', 
          type: 'info',
          visible: true,
        });
      }, 600000); // 10 minutes
    },
  
    resetInactivityTimer(router) {
      this.startInactivityTimer(router);
    },
  
    clearInactivityTimer() {
      if (this.inactivityTimeout) {
        clearTimeout(this.inactivityTimeout);
        this.inactivityTimeout = null;
      }
    },
  },
});
