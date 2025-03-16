<script setup>
import {defineEmits, defineExpose, ref, onMounted, watch} from 'vue';
import { useRecorderStore } from '@/stores/useRecorderStore';

const emits = defineEmits(['answerSent']); 
const recorderStore = useRecorderStore();

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

const clearInput = () => {
    answer.value = '';
}

defineExpose({getAnswer, clearInput});

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
    <input
          type="text"
          v-model="answer"
          class="text-start w-64 md:w-96 text-6xl md:text-8xl border-none self-end p-0 "
          ref="answerInput"
          @mouseover="handleMouseOver"
          placeholder="?"
        />
        </div>
</template>