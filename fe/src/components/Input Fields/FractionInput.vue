<script setup>
import {defineEmits, ref} from 'vue';
const numerator = ref('');
const denominator = ref('');

const emits = defineEmits(['answerSent']); 

function getAnswer() {
    emits('answerSent', numerator.value, denominator.value);
}

defineExpose({getAnswer});
</script>

<template>
    <div class="flex flex-col items-center justify-center">
    <input
          type="text"
          v-model="numerator"
          @keydown="handleKeydown"
          class="text-start w-48 text-8xl border border-gray-300 self-end p-0"
          placeholder="?"
          autofocus
        />
    
    <hr class="w-48 my-2 bg-black border-black border-2 ">
    <input
        type="text"
        v-model="denominator"
        @keydown="handleKeydown"
        class="text-start w-48 text-8xl border border-gray-300 self-end p-0"
        placeholder="?"
        />    

    </div>
</template>