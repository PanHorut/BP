<script setup>
import SubTopic from '@/components/SubTopic.vue';
</script>

<template>
    <h1 class="text-5xl text-center font-bold mt-6">Zlomky</h1>
    <p class="text-center text-2xl mt-20 ">Co vše chceš procvičit?</p>
    <div class="flex justify-center p-11">

        <div class="grid grid-cols-1 md:grid-cols-3 gap-x-20 gap-y-10">
            <SubTopic subtopic="Sčítání a odčítání"></SubTopic>
            <SubTopic subtopic="Násobení a dělení"></SubTopic>
            <SubTopic subtopic="Úprava zlomků"></SubTopic>
        </div>
    </div>
    <div class="flex justify-center">
        <RouterLink to="/examples" class="text-center text-4xl mt-20 border-4 border-blue-600 p-5 rounded-3xl cursor-pointer" >Začít procvičování</RouterLink>
    </div>
</template>