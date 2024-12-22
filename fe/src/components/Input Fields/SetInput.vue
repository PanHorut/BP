<script setup>
import { defineProps, ref, watch, defineEmits, computed, onMounted } from 'vue';

const props = defineProps({
    answer: {
        type: String,
        required: true,
    }
});


const variables = ref([]);
const variableInputs = ref([]);

const emits = defineEmits(['answerSent']); 

function getAnswer() {
    emits('answerSent', variables.value);
}

const clearInput = () => {
    variables.value.forEach(variable => {
        variable.answer = ''; 
    });
};

defineExpose({getAnswer, clearInput});

function getVariables() {
  variables.value = [];

  const pairs = props.answer.split(',').filter(pair => pair);

  pairs.forEach(pair => {
 
    const match = pair.match(/(.*?)\s*\\in\s*(\(.+\))/); 
    
    if (match) {
      const key = match[1].trim();   
      const correctAnswer = match[2].trim(); 

      if (key && correctAnswer) {
        variables.value.push({ key, correctAnswer, answer: '' });
      }
    }
  });

}


watch(() => props.answer, getVariables, { immediate: true });

</script>

<template>
    <div>
        <div v-for="(variable, index) in variables" :key="index" class="flex">
            <p class="flex items-center">{{ computed(() => `\\(${variable.key} \\in \\)`)}} </p>
            <input
                type="text"
                v-model="variable.answer"
                @input="updateAnswers" 
                class="text-start w-64 text-8xl border-none self-end p-0"
                placeholder="?"
            />
        </div>
    </div>
</template>