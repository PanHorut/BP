<script setup>
import {defineEmits,defineExpose, ref} from 'vue';

const emits = defineEmits(['answerSent']); 
const answer = ref('');

function getAnswer() {
    emits('answerSent', answer.value);
}

defineExpose({getAnswer});
</script>

<template>
    <input
          type="text"
          v-model="answer"
          class="text-start w-96 text-8xl border-none self-end p-0"
          placeholder="?"
          autofocus
        />
</template>