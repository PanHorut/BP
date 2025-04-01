<script setup>
import { ref, defineEmits, defineProps, onMounted } from 'vue';

import { useRecorderStore } from "@/stores/useRecorderStore";
import { sendSurveyAnswer } from '@/api/apiClient';
import SpeechVisualizer from './SpeechVisualizer.vue';

const props = defineProps({
  topics: {
    type: Array,
    required: true
  } 
});

const recorderStore = useRecorderStore();
const selectedScale = ref(null);

const toggleRecording = () => {

  if (recorderStore.isRecording) {
    recorderStore.stopRecording();
  } else {
    recorderStore.startRecording(true);
  }
};

const emits = defineEmits(['hideSurvey']);

const storedIndex = sessionStorage.getItem("surveyIndex");

const index = ref(storedIndex ? parseInt(storedIndex, 10) : 0);

const questions = ref([

  { text: "Jak rychle jsi našel cvičení, které jsi chtěl procvičit", type: "scale", boundaries: "Označ: 1 = velmi dlouho, 5 = hned jsem to našel" },

  { text: "Na jakém zařízení aplikaci používáš?", type: "choice", a: "Telefon", b: "Tablet", c: "Počítač" },

  { text: "Bylo něco, co tě při počítání rušilo nebo ti vadilo?", type: "voice" },

  { text: "Vyhovovalo ti více zadávat výsledky hlasem, nebo klávesnicí?", type: "choice", a: "Klávesnicí", b: "Hlasem" },

  { text: "Stalo se ti, že aplikace řekla, že máš chybu, i když jsi měl/a správný výsledek? Pokud ano, jak často?", type: "scale", boundaries: "Označ: 1 = nikdy, 5 = velmi často"},

  { text: "Kdybys mohl/a něco v aplikaci změnit, co by to bylo?", type: "voice" },

  { text: "Jak rychle aplikace reagovala, když jsi řekl výsledek", type: "scale", boundaries: "Označ: 1 = pomalu, 5 = hned!" },

  { text: "Přišlo ti rychlejší říkat výsledky nahlas, nebo je psát na klávesnici?", type: "choice", a: "Nahlas", b: "Na klávesnici" },

  { text: "Stalo se ti, že něco v aplikaci nefungovalo tak, jak mělo? Kde přesně?", type: "voice" },


]);

const handleNext = () => {
  if (recorderStore.isRecording) {
    recorderStore.stopRecording();
  }

  if (index.value < questions.value.length - 1) {
    index.value++;
    sessionStorage.setItem("surveyIndex", index.value.toString()); 
  } else {
    sessionStorage.removeItem("surveyIndex");
    
  }

  emits('hideSurvey');
}

const handleChoiceSelection = async (choice) => {
  await sendSurveyAnswer('choice', questions.value[index.value].text, choice, props.topics);
  handleNext();
}

const sendScaleSelection = async () => {
  if (selectedScale.value === null) {
    return;

  } else {
    await sendSurveyAnswer('scale', questions.value[index.value].text, selectedScale.value, props.topics);
    handleNext();
  }

}

const handleScaleSelection = (num) => {
  selectedScale.value = num;
  console.log("Selected scale:", selectedScale.value);
};

onMounted(() => {
  if (index.value >= 0 && index.value < questions.value.length) {
    recorderStore.updateSurveyQuestionData(questions.value[index.value].text, props.topics);
  } else {
    console.error("Invalid index value:", index.value);
  }
  if (recorderStore.isRecording) {
    recorderStore.stopRecording();
  }
});

</script>

<template>
  <div class="flex flex-col items-center justify-center pt-20 bg-white px-4 text-center ">
    <div class="text-xl md:text-3xl font-semibold text-primary bg-white shadow-xl rounded-xl p-6 w-full max-w-2xl z-20">
      {{ questions[index].text }}
    </div>

    <div class="text-lg md:text-xl flex items-center justify-center mt-6 z-20 text-gray-700 italic">
      <span v-if="questions[index].type == 'voice'">Klikni na mikrofon a odpověz prosím na otázku</span>
      <span v-if="questions[index].type == 'choice'">Vyber možnost která pro tebe platí</span>
      <span v-if="questions[index].type == 'scale'">{{ questions[index].boundaries }}</span>
    </div>

    <!-- Voice answer -->
    <div v-if="questions[index].type == 'voice'" class="flex flex-col items-center justify-center">
      <button @click="toggleRecording"
        :class="recorderStore.isRecording ? 'bg-red-500 hover:bg-red-600 border-red-600' : 'bg-green-500 hover:bg-green-600 border-green-600'"
        class="w-24 h-24 mt-6 flex items-center justify-center rounded-full border-4 text-white text-2xl transition hover:scale-110 shadow-md focus:outline-none z-20"
        :title="recorderStore.isRecording ? 'Stop Recording' : 'Start Recording'">
        <i :class="recorderStore.isRecording ? 'fas fa-stop' : 'fas fa-microphone'" class="text-4xl"></i>
      </button>

      <SpeechVisualizer class="-mt-12 md:mt-0 absolute md:relative z-0"
        :barColor="recorderStore.isRecording ? '#457b9d' : '#f1faee'" :width="300" :height="100" :barWidth="10"
        :barGap="8" :barCount="10" />

      <button @click="handleNext"
        class="mt-8 bg-secondary hover:bg-primary text-white font-semibold py-3 px-6 rounded-lg text-2xl shadow-md transition hover:scale-105">
        Pokračovat
      </button>

    </div>

    <!-- Choice answer -->
    <div v-else-if="questions[index].type == 'choice'">
      <div class="flex flex-col md:flex-row items-center justify-center mt-6 space-y-8 md:space-y-0 md:space-x-16 max-w-lg w-full">
        <button @click="handleChoiceSelection(questions[index].a)"
          class="flex-1 bg-white hover:bg-primary text-primary hover:text-white border-4 border-primary font-semibold py-3 px-6 rounded-2xl text-2xl md:text-3xl shadow-md transition-all transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-sm min-w-[160px] md:min-w-[200px]">
          {{ questions[index].a }}
        </button>

        <button @click="handleChoiceSelection(questions[index].b)"
          class="flex-1 bg-white hover:bg-primary text-primary hover:text-white border-4 border-primary font-semibold py-3 px-6 rounded-2xl text-2xl md:text-3xl shadow-md transition-all transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-sm min-w-[160px] md:min-w-[200px]">
          {{ questions[index].b }}
        </button>

        <button v-if="questions[index].c" @click="handleChoiceSelection(questions[index].c)"
          class="flex-1 bg-white hover:bg-primary text-primary hover:text-white border-4 border-primary font-semibold py-3 px-6 rounded-2xl text-2xl md:text-3xl shadow-md transition-all transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-sm min-w-[160px] md:min-w-[200px]">
          {{ questions[index].c }}
        </button>
      </div>
    </div>
    <div v-else-if="questions[index].type == 'scale'" class="flex flex-col items-center mt-6">


      <div class="flex flex-col justify-center items-center">
        <div class="flex space-x-4">
          <button v-for="num in 5" :key="num" @click="handleScaleSelection(num)"
            class="w-14 h-14 md:w-16 md:h-16 flex items-center justify-center rounded-full border-4 font-bold text-xl md:text-2xl shadow-md transition-all transform hover:scale-110 active:scale-95"
            :class="selectedScale === num ? 'bg-primary text-white border-primary' : 'bg-white text-primary border-primary hover:bg-primary hover:text-white'">
            {{ num }}
          </button>
        </div>
        <button @click="sendScaleSelection()"
          class="mt-8 font-semibold py-3 px-6 rounded-lg text-2xl shadow-md transition transform hover:scale-105"
          :class="selectedScale === null
            ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
            : 'bg-secondary hover:bg-primary text-white cursor-pointer'" :disabled="selectedScale === null">
          Pokračovat
        </button>
      </div>
    </div>

  </div>
</template>