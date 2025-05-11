<!--
================================================================================
 Component: VariableInput.vue
 Description:
        Input field for variable answers.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { defineProps, ref, watch, defineEmits, computed } from 'vue';
import { useRecorderStore } from '@/stores/useRecorderStore';

const props = defineProps({
    answer: {
        type: String,
        required: true,
    }
});
const variables = ref([]);
const recorderStore = useRecorderStore();   

const emits = defineEmits(['answerSent']); 

// Return input fields value to parent component - Example
function getAnswer() {
    emits('answerSent', variables.value);
}

// Clear input fields
const clearInput = () => {
    variables.value.forEach(variable => {
        variable.answer = ''; 
    });
}

// Extract variable names from answer using ';' and '=' as delimiter
function getVariables() {
    variables.value = [];

    const pairs = props.answer.split(';').filter(pair => pair);

    pairs.forEach(pair => {
        const [key, value] = pair.split('=');

        if (key && value !== undefined) {
            variables.value.push({ key: key.trim(), correctAnswer: value.trim(), answer: '' });
        }
    });   
}

defineExpose({getAnswer, clearInput});

// Get variables when the component is mounted
watch(() => props.answer, getVariables, { immediate: true });

// Display users answer by voice if any
watch(
    () => [recorderStore.isRecording, recorderStore.student_answer],
    ([isRecording, studentAnswer]) => {
        if (isRecording && Array.isArray(studentAnswer) && studentAnswer.length) {
            
            studentAnswer.forEach((val, index) => {
                if (variables.value[index]) {
                    variables.value[index].answer = val;
                }
            });

            setTimeout(() => {
                variables.value.forEach(variable => {
                    variable.answer = '';
                });
            }, 1500);
        }
    }
);
</script>

<template>
    <div class="flex flex-col items-end">

        <div v-for="(variable, index) in variables" :key="index" class="flex">

            <!-- Name of variable -->
            <p class="flex items-center">{{ computed(() => `\\(${variable.key}\\)`)}} = </p>

            <!-- Input field for variable -->
            <input
                type="text"
                v-model="variable.answer"
                class="text-start w-64 text-6xl md:text-8xl border-none self-end p-0"
                placeholder="?"
                inputmode="numeric"
                autofocus
            />

        </div>
        
    </div>
</template>
