<script setup>
import { defineProps, computed, ref } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
    skipped: {
        type: Number,
        required: true
    },
    noMistakes: {
        type: Number,
        required: true
    },
    oneMistake: {
        type: Number,
        required: true
    },
    twoMistakes: {
        type: Number,
        required: true
    },
    threeMistakes: {
        type: Number,
        required: true
    }
})

const total = computed(() => {
    return props.skipped + props.noMistakes + props.oneMistake + props.twoMistakes + props.threeMistakes;
});

const getCorrectForm = computed(() => {
    if (total.value === 1) {
        return 'příklad';
    } else if (total.value >= 2 && total.value <= 4) {
        return 'příklady';
    } else {
        return 'příkladů';
    }
});
// Calculate percentages for each category
const percentages = computed(() => {
    return {
        skipped: (props.skipped / total.value) * 100,
        noMistakes: (props.noMistakes / total.value) * 100,
        oneMistake: (props.oneMistake / total.value) * 100,
        twoMistakes: (props.twoMistakes / total.value) * 100,
        threeMistakes: (props.threeMistakes / total.value) * 100
    };
});
</script>

<template>
    <div class="flex flex-col items-center justify-center mt-24 border-4 border-secondary rounded-xl px-24 py-4">
        <h1 class="text-6xl font-bold text-primary">Hotovo!</h1>
        <h2 class="text-2xl font-semibold text-primary text-center mt-4">Spočítal jsi {{ total }} {{ getCorrectForm }}</h2>

        <!-- Multiple Value Bar -->
        <div class="w-full max-w-3xl h-12 flex rounded-full overflow-hidden mt-12">
            <!-- Skipped -->
            <div 
                class="bg-gray-400 h-full tooltip" 
                :style="{ width: percentages.skipped + '%' }"
                data-tooltip="Přeskočeno: {{ props.skipped }}"
            ></div>
            
            <!-- No Mistakes -->
            <div 
                class="bg-green-500 h-full tooltip" 
                :style="{ width: percentages.noMistakes + '%' }"
                data-tooltip="Bez chyb: {{ props.noMistakes }}"
            ></div>

            <!-- One Mistake -->
            <div 
                class="bg-yellow-400 h-full tooltip" 
                :style="{ width: percentages.oneMistake + '%' }"
                data-tooltip="Jedna chyba: {{ props.oneMistake }}"
            ></div>

            <!-- Two Mistakes -->
            <div 
                class="bg-orange-400 h-full tooltip" 
                :style="{ width: percentages.twoMistakes + '%' }"
                data-tooltip="Dvě chyby: {{ props.twoMistakes }}"
            ></div>

            <!-- Three Mistakes -->
            <div 
                class="bg-red-500 h-full tooltip" 
                :style="{ width: percentages.threeMistakes + '%' }"
                data-tooltip="Tři chyby: {{ props.threeMistakes }}"
            ></div>
        </div>

        <!-- Legend -->
        <div class="flex justify-center space-x-4 mt-4">
            <div v-if="props.skipped > 0" class="flex items-center">
                <span class="block w-4 h-4 bg-gray-400 rounded-full"></span>
                <span class="ml-2">Přeskočeno ({{ props.skipped }})</span>
            </div>
            <div v-if="props.noMistakes > 0" class="flex items-center">
                <span class="block w-4 h-4 bg-green-500 rounded-full"></span>
                <span class="ml-2">Bez chyby ({{ props.noMistakes }})</span>
            </div>
            <div v-if="props.oneMistake > 0" class="flex items-center">
                <span class="block w-4 h-4 bg-yellow-400 rounded-full"></span>
                <span class="ml-2">Jedna chyba ({{ props.oneMistake }})</span>
            </div>
            <div v-if="props.twoMistakes > 0" class="flex items-center">
                <span class="block w-4 h-4 bg-orange-400 rounded-full"></span>
                <span class="ml-2">Dvě chyby ({{ props.twoMistakes }})</span>
            </div>
            <div v-if="props.threeMistakes > 0" class="flex items-center">
                <span class="block w-4 h-4 bg-red-500 rounded-full"></span>
                <span class="ml-2">Tři chyby ({{ props.threeMistakes }})</span>
            </div>
        </div>

        <div class="flex justify-center mt-16 mb-6">
            <RouterLink to="/" class="text-center text-3xl bg-secondary hover:bg-white text-white hover:text-secondary border-4 border-secondary rounded-xl font-semibold px-4 py-2 cursor-pointer">
                Zpět na hlavní stránku
            </RouterLink>
        </div>
    </div>
</template>

<style scoped>
.tooltip {
    position: relative;
    cursor: pointer;
}

.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background-color: black;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}

.tooltip:hover::after {
    opacity: 1;
}
</style>
