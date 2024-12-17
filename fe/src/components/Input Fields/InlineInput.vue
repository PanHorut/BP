<script setup>
import {defineEmits,defineExpose, ref, onMounted} from 'vue';

const emits = defineEmits(['answerSent']); 
const answer = ref('');
const answerInput = ref(null);

function getAnswer() {
    emits('answerSent', answer.value);
}

onMounted(() => {
    if (answerInput.value) {
        answerInput.value.focus();
    }
});

function handleMouseOver() {
    answerInput.value.focus();
}

defineExpose({getAnswer});
</script>

<template>
    <input
          type="text"
          v-model="answer"
          class="text-start w-96 text-8xl border-none self-end p-0"
          ref="answerInput"
          @mouseover="handleMouseOver"
          placeholder="?"
        />
</template>