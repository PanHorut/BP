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

function getAnswer() {
    emits('answerSent', variables.value);
}

const clearInput = () => {
    variables.value.forEach(variable => {
        variable.answer = ''; 
    });
}

defineExpose({getAnswer, clearInput});

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

watch(() => props.answer, getVariables, { immediate: true });

function updateAnswers() {
    const answers = variables.value.reduce((acc, variable) => {
        acc[variable.key] = variable.answer;
        return acc;
    }, {});
    //emits('updateAnswers', answers);
}

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
    <div>
        <div v-for="(variable, index) in variables" :key="index" class="flex">
            <p class="flex items-center">{{ computed(() => `\\(${variable.key}\\)`)}} = </p>
            <input
                type="text"
                v-model="variable.answer"
                @input="updateAnswers" 
                class="text-start w-64 text-6xl md:text-8xl border-none self-end p-0"
                placeholder="?"
                autofocus
            />
        </div>
    </div>
</template>
