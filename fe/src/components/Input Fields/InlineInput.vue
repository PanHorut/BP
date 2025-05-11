<!--
================================================================================
 Component: InlineInput.vue
 Description:
        Input field for answers in inline form.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { defineEmits, defineExpose, ref, onMounted, watch } from 'vue';
import { useRecorderStore } from '@/stores/useRecorderStore';

const emits = defineEmits(['answerSent']);
const recorderStore = useRecorderStore();

//
const answer = ref('');
const answerInput = ref(null);

// Return input field value to parent component - Example
function getAnswer() {
    emits('answerSent', answer.value);
}

// Focus on the input field when the component is mounted
onMounted(() => {
    if (answerInput.value && !recorderStore.isRecording) {
        answerInput.value.focus();
    }
});

// Focus on the input field when mouse is over it
function handleMouseOver() {
    answerInput.value.focus();
}

// Clear input field
const clearInput = () => {
    answer.value = '';
}

defineExpose({ getAnswer, clearInput });

// Display users answer by voice if any
watch(
    () => [recorderStore.isRecording, recorderStore.student_answer],
    ([isRecording, studentAnswer]) => {
        if (isRecording && studentAnswer) {
            answer.value = studentAnswer;

            setTimeout(() => {
                answer.value = '';
            }, 1500);
        }
    }
);
</script>

<template>
    <div class="flex items-center justify-center">

        <input v-model="answer" class="text-start w-64 md:w-96 text-6xl md:text-8xl border-none self-end p-0"
            ref="answerInput" @mouseover="handleMouseOver" placeholder="?" inputmode="numeric" />
    </div>
</template>