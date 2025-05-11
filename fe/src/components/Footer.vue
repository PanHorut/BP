<!--
================================================================================
 Component: Footer.vue
 Description:
        Displays footer of the application.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { dictionary } from '@/utils/dictionary';
import { useLanguageStore } from '@/stores/useLanguageStore';

const langStore = useLanguageStore();
</script>

<template>

    <footer class="flex items-center justify-center bg-primary text-center py-4 h-24">
        
        <p class="text-white text-xl font-semibold"><i class="fa-regular fa-copyright"></i> 2025 {{ dictionary[langStore.language].logo }}</p>

    </footer>

</template>