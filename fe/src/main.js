import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { useAuthStore } from '@/stores/useAuthStore';


import App from './App.vue';
import router from './router';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.mount('#app');

const authStore = useAuthStore();
authStore.loadStoredSession();


