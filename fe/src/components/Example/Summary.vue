<script setup>
import {defineProps} from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
    time:{
        type: Number,
        //required: true
    },
    total:{
        type: Number,
        required: true
    },
    skipped:{
        type: Number,
        required: true
    },
    mistakes:{
        type: Number,
        required: true
    }
})

</script>

<template>
    <div class="flex flex-col items-center justify-center mt-24 border-4 border-primary rounded-xl px-24 py-4">
        <h1 class="text-6xl font-bold text-primary">Hotovo!</h1>
        <p class="text-3xl mt-8">Celkem jsi spočítal <span class="font-black text-4xl">{{ props.total}}</span> {{ props.total > 4 ? 'příkladů' : 'příklady'}}</p>
        <div class="text-2xl mt-4 flex flex-col items-center">
            <p>Z toho jsi <span class="font-black text-3xl text-red-600">{{ props.mistakes }}x</span> nespočítal příklad správně </p>
            <p>a <span class="font-black text-3xl">{{ props.skipped }}</span> {{ props.skipped > 4 ? 'příkladů' : 'příklady'}} jsi přeskočil </p>
        </div>

        <div class="flex justify-center mt-16 mb-6">
            <RouterLink to="/"  class="text-center text-3xl bg-secondary hover:bg-white text-white hover:text-secondary border-4 border-secondary rounded-xl font-semibold px-4 py-2 cursor-pointer">Zpět na hlavní stránku</RouterLink>
        </div>
    </div>
</template>