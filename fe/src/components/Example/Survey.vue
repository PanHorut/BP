<script setup>
import { ref, defineEmits, defineProps, onMounted } from 'vue';

import { useRecorderStore } from "@/stores/useRecorderStore";
import { sendSurveyAnswer } from '@/api/apiClient';
import SpeechVisualizer from './SpeechVisualizer.vue';
import { dictionary } from '@/utils/dictionary';
import { useLanguageStore } from '@/stores/useLanguageStore'; 

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

const langStore = useLanguageStore();

const storedIndex = sessionStorage.getItem("surveyIndex");

const index = ref(storedIndex ? parseInt(storedIndex, 10) : 0);

const questions = ref([
  { 
    text: { 
      cs: "Jak rychle jsi našel cvičení, které jsi chtěl procvičit?", 
      en: "How quickly did you find the exercise you wanted to practice?" 
    }, 
    type: "scale", 
    boundaries: { 
      cs: "Označ: 1 = velmi dlouho, 5 = hned jsem to našel", 
      en: "Mark: 1 = took a long time, 5 = found it immediately" 
    } 
  },
  { 
    text: { 
      cs: "Na jakém zařízení aplikaci používáš?", 
      en: "On which device do you use the app?" 
    }, 
    type: "choice", 
    a: { cs: "Telefon", en: "Phone" }, 
    b: { cs: "Tablet", en: "Tablet" }, 
    c: { cs: "Počítač", en: "Computer" } 
  },
  { 
    text: { 
      cs: "Bylo něco, co tě při počítání rušilo nebo ti vadilo?", 
      en: "Was there anything that distracted or bothered you while solving problems?" 
    }, 
    type: "voice" 
  },
  { 
    text: { 
      cs: "Vyhovovalo ti více zadávat výsledky hlasem, nebo klávesnicí?", 
      en: "Did you prefer entering results by voice or keyboard?" 
    }, 
    type: "choice", 
    a: { cs: "Klávesnicí", en: "Keyboard" }, 
    b: { cs: "Hlasem", en: "Voice" } 
  },
  { 
    text: { 
      cs: "Stalo se ti, že aplikace řekla, že máš chybu, i když jsi měl/a správný výsledek? Pokud ano, jak často?", 
      en: "Did the app ever say you were wrong even though you gave the correct answer? If so, how often?" 
    }, 
    type: "scale", 
    boundaries: { 
      cs: "Označ: 1 = nikdy, 5 = velmi často", 
      en: "Mark: 1 = never, 5 = very often" 
    } 
  },
  { 
    text: { 
      cs: "Kdybys mohl/a něco v aplikaci změnit, co by to bylo?", 
      en: "If you could change anything in the app, what would it be?" 
    }, 
    type: "voice" 
  },
  { 
    text: { 
      cs: "Jak rychle aplikace reagovala, když jsi řekl výsledek?", 
      en: "How quickly did the app respond when you said the result?" 
    }, 
    type: "scale", 
    boundaries: { 
      cs: "Označ: 1 = pomalu, 5 = hned!", 
      en: "Mark: 1 = slowly, 5 = instantly!" 
    } 
  },
  { 
    text: { 
      cs: "Přišlo ti rychlejší říkat výsledky nahlas, nebo je psát na klávesnici?", 
      en: "Did you find it faster to say the results out loud or type them on the keyboard?" 
    }, 
    type: "choice", 
    a: { cs: "Nahlas", en: "Out loud" }, 
    b: { cs: "Na klávesnici", en: "On the keyboard" } 
  },
  { 
    text: { 
      cs: "Stalo se ti, že něco v aplikaci nefungovalo tak, jak mělo? Kde přesně?", 
      en: "Did anything in the app not work as expected? Where exactly?" 
    }, 
    type: "voice" 
  }
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
      {{ questions[index].text[langStore.language] }}
    </div>

    <div class="text-lg md:text-xl flex items-center justify-center mt-6 z-20 text-gray-700 italic">
      <span v-if="questions[index].type == 'voice'">{{dictionary[langStore.language].clickMicText}}</span>
      <span v-if="questions[index].type == 'choice'">{{dictionary[langStore.language].chooseOptionText}}</span>
      <span v-if="questions[index].type == 'scale'">{{ questions[index].boundaries[langStore.language] }}</span>
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
        {{dictionary[langStore.language].continue}}
      </button>

    </div>

    <!-- Choice answer -->
    <div v-else-if="questions[index].type == 'choice'">
      <div class="flex flex-col md:flex-row items-center justify-center mt-6 space-y-8 md:space-y-0 md:space-x-16 max-w-lg w-full">
        <button @click="handleChoiceSelection(questions[index].a[langStore.language])"
          class="flex-1 bg-white hover:bg-primary text-primary hover:text-white border-4 border-primary font-semibold py-3 px-6 rounded-2xl text-2xl md:text-3xl shadow-md transition-all transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-sm min-w-[160px] md:min-w-[200px]">
          {{ questions[index].a[langStore.language] }}
        </button>

        <button @click="handleChoiceSelection(questions[index].b[langStore.language])"
          class="flex-1 bg-white hover:bg-primary text-primary hover:text-white border-4 border-primary font-semibold py-3 px-6 rounded-2xl text-2xl md:text-3xl shadow-md transition-all transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-sm min-w-[160px] md:min-w-[200px]">
          {{ questions[index].b[langStore.language] }}
        </button>

        <button v-if="questions[index].c" @click="handleChoiceSelection(questions[index].c[langStore.language])"
          class="flex-1 bg-white hover:bg-primary text-primary hover:text-white border-4 border-primary font-semibold py-3 px-6 rounded-2xl text-2xl md:text-3xl shadow-md transition-all transform hover:scale-110 hover:shadow-lg active:scale-95 active:shadow-sm min-w-[160px] md:min-w-[200px]">
          {{ questions[index].c[langStore.language] }}
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
          {{ dictionary[langStore.language].continue }}
        </button>
      </div>
    </div>

  </div>
</template>