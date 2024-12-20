<script setup>
import { ref, defineProps } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
});

// Predefined input types
const inputTypes = [
  { label: 'Psaná odpověď', value: 'text' },
  { label: 'Rozhodovačka', value: 'decision' },
  { label: 'Radio', value: 'radio' },
];

const selectedInputType = ref(props.modelValue);
</script>

<template>
    <div class="w-full flex justify-start items-center">
      <label class=" text-primary text-xl font-bold my-8 mr-2" for="inputTypeSelect">
        Typ cvičení
      </label>
      <select
        id="inputTypeSelect"
        v-model="selectedInputType"
        class="block w-64 bg-white border border-gray-300 text-primary py-2 px-3 pr-8 rounded-lg focus:outline-none focus:border-blue-500"
        @change="$emit('update:modelValue', selectedInputType)"
      >
        <option v-for="type in inputTypes" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>
    </div>
  </template>
  

  