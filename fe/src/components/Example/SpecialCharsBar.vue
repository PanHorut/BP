<script setup>

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
    <div @mousedown.prevent class="fixed bottom-0 w-full pb-10 border-t-4 border-primary">
        <div class="flex flex-col items-center">
            <div class="text-center text-primary text-3xl font-black my-4">Speciální znaky</div>
            <div class="flex justify-center gap-4">
            <button 
              @click="insertTextIntoActiveInput('&#8734;')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-4xl flex items-center justify-center" 
              >&#8734;
            </button>
            <button 
              @click="insertTextIntoActiveInput('x²')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-4xl flex items-center justify-center" 
              >x<sup>2</sup>
            </button>
            <button 
              @click="insertTextIntoActiveInput('x³')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-4xl flex items-center justify-center" 
              >x<sup>3</sup>
            </button>
            <button 
              @click="insertTextIntoActiveInput('<')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-4xl flex items-center justify-center" 
              ><
            </button>
            <button 
              @click="insertTextIntoActiveInput('>')" 
              class="w-16 h-16 bg-primary rounded-xl text-white font-black text-4xl flex items-center justify-center" 
              >>
            </button>

            

            

            
        </div>
        </div>
    </div>
</template>


