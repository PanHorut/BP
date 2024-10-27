<script setup>

const props = defineProps({
    subtopic: {
    type: String,
    default: 'Bez tématu',
    }
});
</script>

<template>
    <div class="flex items-center space-x-2">
    <input id="custom-checkbox" type="checkbox" class="w-8 h-8 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
    <h1 class="text-2xl">{{ subtopic }}</h1>
</div>
</template>