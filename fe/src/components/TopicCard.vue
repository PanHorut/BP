<script setup>
import {ref, computed } from 'vue';
import { RouterLink, useRoute } from 'vue-router';


const props = defineProps({
    topic: {
    type: String,
    default: 'Bez tématu',
    }
});

</script>

<template>
    <div class="border border-gray-300 rounded-lg shadow-lg max-w-md bg-white">

        <RouterLink to="/topics" class="flex justify-center text-2xl text-center font-bold text-gray-800 p-4">
        
           {{ topic }}
        </RouterLink>
        
        
    </div>

</template>