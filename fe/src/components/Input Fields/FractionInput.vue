<script setup>
import { ref, onMounted, defineExpose, defineEmits, watch } from 'vue';
import { useRecorderStore } from '@/stores/useRecorderStore';

const numerator = ref('');
const denominator = ref('');
const numeratorInput = ref(null); 
const denominatorInput = ref(null); 

const recorderStore = useRecorderStore();

const emits = defineEmits(['answerSent']); 

function getAnswer() {
    emits('answerSent', numerator.value, denominator.value);
}

onMounted(() => {
    if (numeratorInput.value) {
        numeratorInput.value.focus();
    }
});

function handleMouseOver(refName) {
    if (refName == numeratorInput.value) {
        numeratorInput.value.focus();
    } else if (refName == denominatorInput.value) {
        denominatorInput.value.focus();
    }
}

function handleKeydown(event) {
    if (event.key === 'ArrowDown' && event.target === numeratorInput.value) {
        denominatorInput.value.focus();
    } else if (event.key === 'ArrowUp' && event.target === denominatorInput.value) {
        numeratorInput.value.focus();
    }
}

const clearInput = () => {
    numerator.value = '';
    denominator.value = '';
    
}

defineExpose({getAnswer, clearInput});

watch(
    () => [recorderStore.isRecording, recorderStore.student_answer],
    ([isRecording, studentAnswer]) => {
        if (isRecording && studentAnswer) {
            numerator.value = studentAnswer.numerator;
            denominator.value = studentAnswer.denominator;

            setTimeout(() => {
                numerator.value = '';
                denominator.value = '';
            }, 1500);
        }
    }
);
</script>

<template>
    <div class="flex flex-col items-center justify-center">
        <input
            type="text"
            v-model="numerator"
            ref="numeratorInput"
            @keydown="handleKeydown"
            @mouseover="handleMouseOver(numeratorInput)"
            class="text-start w-48 text-8xl border border-gray-300 self-end p-0"
            placeholder="?"
        />
    
        <hr class="w-48 my-2 bg-black border-black border-2 ">
        
        <input
            type="text"
            v-model="denominator"
            ref="denominatorInput"
            @keydown="handleKeydown"
            @mouseover="handleMouseOver(denominatorInput)"
            class="text-start w-48 text-8xl border border-gray-300 self-end p-0"
            placeholder="?"
        />    
    </div>
</template>
