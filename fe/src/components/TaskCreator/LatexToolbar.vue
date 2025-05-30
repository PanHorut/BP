<!--
================================================================================
 Component: LatexToolbar.vue
 Description:
        Allows admin to insert Latex symbols into the input fields
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';

// Defined latex symbols
const frac = computed(() => `\\(\\frac{a}{b}\\)`);
const pwr2 = computed(() => `\\(a^2\\)`);
const pwr3 = computed(() => `\\(a^3\\)`);
const pwrn = computed(() => `\\(a^n\\)`);
const bcurly = computed(() => `\\(\\{ \\}\\)`);
const bround = computed(() => `\\(( )\\)`);
const bsquare = computed(() => `\\([ ]\\)`);
const sqroot = computed(() => `\\(\\sqrt{a}\\)`);
const root = computed(() => `\\(\\sqrt[n]{a}\\)`);
const isin = computed(() => `\\(\\in\\)`);
const notin = computed(() => `\\(\\notin\\)`);
const inf = computed(() => `\\(\\infty\\)`);
const real = computed(() => `\\(\\mathbb{R}\\)`);
const times = computed(() => `\\(\\cdot\\)`);
const mutliline = computed(() => `\\(\\begin{align*} a = b \\\\ c = d \\end{align*}\\)`); 

// Render latex
function renderMathJax() {
  if (window.MathJax) {
    window.MathJax.typeset();
  }
}

// Hide toolbar on small screens
const isHidden = ref(window.innerWidth < 1100);

// Check window size and hide toolbar if necessary
const checkWindowSize = () => {
  isHidden.value = window.innerWidth < 1100;
};

// Watch for window resize events
onMounted(() => {
  renderMathJax();
  window.addEventListener('resize', checkWindowSize);
  checkWindowSize(); 
});

// Cleanup event listener on component unmount
onUnmounted(() => {
  window.removeEventListener('resize', checkWindowSize);
});

// Toggle toolbar visibility
const toggleToolbar = () => {
  isHidden.value = !isHidden.value;
}

// Insert latex into currently focused input field
function insertTextIntoActiveInput(text) {
  const activeElement = document.activeElement;

  // Check if the active element is an input or textarea
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
    <div @mousedown.prevent :class="['fixed left-0 h-full border-r-4 border-t-4 border-primary w-56 transition-transform duration-300', 
              { '-translate-x-48': isHidden, 'translate-x-0': !isHidden }]">

        <div class="flex flex-col items-center">
            <div class="text-center text-primary text-3xl font-black my-4">LaTeX zápis</div>
            
            <!-- Buttons for each symbol -->
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

            <button 
              @click="insertTextIntoActiveInput('\\in')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="isin">
            </button>

            <button 
              @click="insertTextIntoActiveInput('\\notin')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="notin">
            </button>

            <button 
              @click="insertTextIntoActiveInput('\\infty')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="inf">
            </button>

            <button 
              @click="insertTextIntoActiveInput('\\mathbb{R}')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="real">
            </button>
            <button 
              @click="insertTextIntoActiveInput('\\cdot')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-3xl flex items-center justify-center" 
              v-html="times">
            </button>
            <button 
              @click="insertTextIntoActiveInput('\\begin{align*} a = b \\\\ c = d \\end{align*}')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-xl flex items-center justify-center" 
              v-html="mutliline">
            </button>
        </div>

        </div>

        <!-- Button to toggle toolbar visibility -->
        <div 
          @click="toggleToolbar" 
          class="fixed top-1/2 left-56 -translate-y-1/2 ml-2 bg-primary text-white text-2xl  cursor-pointer font-bold w-12 h-12 rounded-full flex items-center justify-center"
        >
          {{ isHidden ? '>' : '<' }}
        </div>

    </div>
</template>