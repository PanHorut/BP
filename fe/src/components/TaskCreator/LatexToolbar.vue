<script setup>
import { computed, onMounted, watch } from 'vue';

const frac = computed(() => `\\(\\frac{a}{b}\\)`);
const pwr2 = computed(() => `\\(a^2\\)`);
const pwr3 = computed(() => `\\(a^3\\)`);
const pwrn = computed(() => `\\(a^n\\)`);
const bcurly = computed(() => `\\(\\{ \\}\\)`);
const bround = computed(() => `\\(( )\\)`);
const bsquare = computed(() => `\\([ ]\\)`);
const sqroot = computed(() => `\\(\\sqrt{a}\\)`);
const root = computed(() => `\\(\\sqrt[n]{a}\\)`);





function renderMathJax() {
  if (window.MathJax) {
    window.MathJax.typeset();
  }
}

onMounted(() => {
  renderMathJax();
});

watch(frac, () => {
  renderMathJax();
});

function insertTextIntoActiveInput(text) {
  const activeElement = document.activeElement;

  if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
    const start = activeElement.selectionStart;
    const end = activeElement.selectionEnd;

    const value = activeElement.value;
    activeElement.value = value.slice(0, start) + text + value.slice(end);
    activeElement.selectionStart = activeElement.selectionEnd = start + text.length;

    activeElement.dispatchEvent(new Event('input'));
  }
}
</script>

<template>
    <div @mousedown.prevent class="fixed left-0 h-full border-r-4 border-t-4 border-primary w-56">
        <div class="flex flex-col items-center">
            <div class="text-center text-primary text-3xl font-black my-4">LaTeX zápis</div>
            <!-- Render frac using v-html for MathJax processing and center content -->
            <div class="grid grid-cols-2 justify-center gap-4">
            <button 
              @click="insertTextIntoActiveInput('\\frac{a}{b}')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="frac">
            </button>

            <button 
              @click="insertTextIntoActiveInput('a^2')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="pwr2">
            </button>

            <button 
              @click="insertTextIntoActiveInput('a^3')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="pwr3">
            </button>

            <button 
              @click="insertTextIntoActiveInput('a^{n}')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="pwrn">
            </button>

            <button 
              @click="insertTextIntoActiveInput('()')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="bround">
            </button>

            <button 
              @click="insertTextIntoActiveInput('[]')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="bsquare">
            </button>

            <button 
              @click="insertTextIntoActiveInput('\\{\\}')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="bcurly">
            </button>

            <button 
              @click="insertTextIntoActiveInput('\\sqrt{a}')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="sqroot">
            </button>

            <button 
              @click="insertTextIntoActiveInput('\\sqrt[n]{a}')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="root">
            </button>
        </div>
        </div>
    </div>
</template>


