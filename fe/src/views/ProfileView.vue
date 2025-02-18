<script setup>
import Signup from '@/components/Profile/Signup.vue';
import Login from '@/components/Profile/Login.vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { RouterLink } from 'vue-router';
import {ref} from 'vue';

const authStore = useAuthStore();
const showLogin = ref(true);

const toggleLogin = () => {
  showLogin.value = !showLogin.value;
}   



</script>

<template>
    <div v-if="authStore.isAuthenticated" class="w-full text-4xl text-primary flex flex-col items-center justify-center font-bold pt-12">
        <p>Ahoj {{ authStore.name }}!</p>
        <p class="mt-12 text-3xl text-secondary font-semibold">Na této stránce brzy uvidíš statistiky o tom, jak počítáš :-)</p>

    </div>
    
    <div v-else>
        <Login v-if="showLogin"/>
        <Signup v-else/>

        <button @click="toggleLogin" class="underline w-full text-secondary text-lg">{{ showLogin ? "Ještě nemám účet - registrovat se" : "Už mám účet - přihlásit se" }}</button>
        <RouterLink to="/admin" class="underline w-full text-secondary text-lg mt-12 flex justify-center">Jsem administrátor aplikace</RouterLink>
    </div>


</template>
  