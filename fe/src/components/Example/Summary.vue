<script setup>
import {defineProps} from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
    time:{
        type: Number,
        required: true
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
        <p class="text-2xl mt-4">
            Z toho jsi <span>{{ props.mistakes }}x</span> udělal chybu a <span>{{ props.skipped }}x</span> příklad přeskočil  
        </p>

        <div class="flex justify-center">
            <RouterLink to="/"  class="text-center text-4xl cursor-pointer">Zpět na hlavní stránku</RouterLink>
        </div>
    </div>
</template>