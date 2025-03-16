<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const showTips = ref(false);
const isMobile = ref(false);

const toggleShowTips = () => {
    showTips.value = !showTips.value;
};

const checkIfMobile = () => {
    isMobile.value = window.matchMedia('(max-width: 768px)').matches;
};

// Listen for screen size changes
onMounted(() => {
    checkIfMobile();
    window.addEventListener('resize', checkIfMobile);
});

// Cleanup event listener
onBeforeUnmount(() => {
    window.removeEventListener('resize', checkIfMobile);
});
</script>

<template>
    <div class="relative z-40">
        <button 
            @click="isMobile ? toggleShowTips() : null" 
            @mouseenter="!isMobile ? showTips = true : null" 
            @mouseleave="!isMobile ? showTips = false : null"
            class="text-3xl font-bold text-gray-700 bg-gray-200 w-12 h-12 
            flex items-center justify-center rounded-full border-4 border-gray-500
            transition ease-in-out hover:bg-gray-300 hover:border-gray-700 hover:scale-105 shadow-md relative md:z-50">
            ?
        </button>

        <div v-if="showTips" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 
            w-11/12 md:w-1/2 bg-white border border-gray-300 shadow-2xl rounded-xl p-6 text-lg 
            text-gray-800  transition-all duration-300 ease-in-out">
            <h3 class="text-xl font-bold text-center mb-4 text-primary">Tipy pro zadávání hlasem</h3>
            <button v-if="isMobile" @click="showTips = false" class="absolute top-4 right-4 text-4xl text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
            </button>
            <ul class="list-disc pl-6 space-y-8">
                <li class="flex flex-col space-y-2 pb-2 border-b border-gray-300 text-[15px] md:text-lg">
                    <span class="flex items-center font-semibold">
                        Pro zadávání hlasem stiskni
                        <div class="w-8 h-8 rounded-full bg-green-500 flex justify-center items-center ml-2 shadow-md">
                            <i class="fas fa-microphone text-white"></i>
                        </div>
                    </span>
                </li>

                <li class="flex flex-col space-y-2 pb-2 border-b border-gray-300 text-[15px] md:text-lg">
                    <span class="flex items-center font-semibold">
                        Pro ukončení zadávání hlasem stiskni
                        <div class="w-8 h-8 rounded-full bg-red-500 flex justify-center items-center ml-2 shadow-md">
                            <i class="fas fa-stop text-white"></i>
                        </div>
                    </span>
                </li>

                <li class="flex flex-col space-y-1 pb-2 border-b border-gray-300 text-sm md:text-lg">
                    <span class="font-semibold">Pokud je výsledek ve tvaru zlomku, vyslov jej jako:</span>
                    <span class="ml-4"><span class="font-bold">čitatel LOMENO (nebo DĚLENO) jmenovatel</span></span>
                    <span class="italic text-gray-500 ml-4">např. "dva lomeno tři", "osm děleno pět"</span>
                </li>

                <li class="flex flex-col space-y-1 text-sm md:text-lg">
                    <span class="font-semibold">Výsledek proměnné vyslov jako:</span>
                    <span class="ml-4"><span class="font-bold">název proměnné ROVNÁ SE (nebo JE) hodnota</span></span>
                    <span class="italic text-gray-500 ml-4">např. "x je patnáct", "y je dva"</span>
                </li>
            </ul>
        </div>
    </div>
</template>
