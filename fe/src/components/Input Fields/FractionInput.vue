<!--
================================================================================
 Component: FractionInput.vue
 Description:
        Input fields for answers in fraction form.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, onMounted, defineExpose, defineEmits, watch } from 'vue';
import { useRecorderStore } from '@/stores/useRecorderStore';

const numerator = ref('');
const denominator = ref('');
const numeratorInput = ref(null); 
const denominatorInput = ref(null); 

const recorderStore = useRecorderStore();

const emits = defineEmits(['answerSent']); 

// Return input fields value to parent component - Example
function getAnswer() {
    emits('answerSent', numerator.value, denominator.value);
}

// Focus on the numerator input field when the component is mounted
onMounted(() => {
    if (numeratorInput.value && !recorderStore.isRecording) {
        numeratorInput.value.focus();
    }
});

// Focus on the input field when mouse is over it
function handleMouseOver(refName) {
    if (refName == numeratorInput.value) {
        numeratorInput.value.focus();
    } else if (refName == denominatorInput.value) {
        denominatorInput.value.focus();
    }
}

// Handle keydown events for navigating between input fields
function handleKeydown(event) {
    if (event.key === 'ArrowDown' && event.target === numeratorInput.value) {
        denominatorInput.value.focus();
    } else if (event.key === 'ArrowUp' && event.target === denominatorInput.value) {
        numeratorInput.value.focus();
    }
}

// Clear input fields
const clearInput = () => {
    numerator.value = '';
    denominator.value = '';
}

defineExpose({getAnswer, clearInput});

// Display users answer by voice if any
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

        <!-- Numerator input -->
        <input
            type="text"
            v-model="numerator"
            ref="numeratorInput"
            @keydown="handleKeydown"
            @mouseover="handleMouseOver(numeratorInput)"
            class="text-start w-32 md:w-48 text-6xl md:text-8xl border border-gray-300 self-end p-0"
            placeholder="?"
            inputmode="numeric"
        />
        
        <!-- Fraction line -->
        <hr class="w-32 md:w-48 my-2 bg-black border-black border-2 ">
        
        <!-- Denominator input -->
        <input
            type="text"
            v-model="denominator"
            ref="denominatorInput"
            @keydown="handleKeydown"
            @mouseover="handleMouseOver(denominatorInput)"
            class="text-start w-32 md:w-48 text-6xl md:text-8xl border border-gray-300 self-end p-0"
            placeholder="?"
            inputmode="numeric"
        />   

    </div>
</template>
