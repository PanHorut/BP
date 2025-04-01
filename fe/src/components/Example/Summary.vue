<script setup>
import { defineProps, computed, ref } from 'vue';
import { sendSurveyAnswer } from '@/api/apiClient';
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
    },
    topics: {
    type: Array,
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

const selectedEmoji = ref(null);

const emojiRatings = ref([
    { icon: "fas fa-frown", label: "Nelíbilo se mi to." },
    { icon: "fas fa-meh", label: "Nic moc, mohlo by to být lepší." },
    { icon: "fas fa-smile", label: "Dobré, ale něco bych zlepšil/a." },
    { icon: "fas fa-smile-beam", label: "Super! Bavilo mě to." },
]);

const handleEmojiSelection = async () => {
    if(selectedEmoji.value === null) {
        return;
    }

    await sendSurveyAnswer('summary', 'Jak se ti líbilo procvičování s touto aplikací?', emojiRatings.value[selectedEmoji.value].label, props.topics);  

}

</script>

<template>
    <div
        class="flex flex-col items-center justify-center mt-12 md:mt-24 md:border-4 md:border-secondary rounded-xl px-12 md:px-24 py-4 max-w-full">
        <h1 class="text-5xl md:text-6xl font-bold text-primary">Hotovo!</h1>
        <h2 class="text-lg md:text-2xl font-semibold text-primary text-center mt-4">
            Spočítal jsi {{ total }} {{ getCorrectForm }}
        </h2>

        <!-- Multiple Value Bar -->
        <div class="w-full md:max-w-3xl h-8 md:h-12 flex rounded-full overflow-hidden mt-8 md:mt-12">
            <!-- Skipped -->
            <div class="bg-gray-400 h-full" :style="{ width: percentages.skipped + '%' }"
                data-tooltip="Přeskočeno: {{ props.skipped }}"></div>

            <!-- No Mistakes -->
            <div class="bg-green-500 h-full" :style="{ width: percentages.noMistakes + '%' }"
                data-tooltip="Bez chyb: {{ props.noMistakes }}"></div>

            <!-- One Mistake -->
            <div class="bg-yellow-400 h-full" :style="{ width: percentages.oneMistake + '%' }"
                data-tooltip="Jedna chyba: {{ props.oneMistake }}"></div>

            <!-- Two Mistakes -->
            <div class="bg-orange-400 h-full " :style="{ width: percentages.twoMistakes + '%' }"
                data-tooltip="Dvě chyby: {{ props.twoMistakes }}"></div>

            <!-- Three Mistakes -->
            <div class="bg-red-500 h-full" :style="{ width: percentages.threeMistakes + '%' }"
                data-tooltip="Tři chyby: {{ props.threeMistakes }}"></div>
        </div>

        <!-- Legend -->
        <div class="grid grid-cols-1 md:flex md:justify-center md:space-x-4 mt-4 text-lg font-medium md:text-base">
            <div v-if="props.skipped > 0" class="flex items-center space-x-2">
                <span class="block w-3 h-3 md:w-4 md:h-4 bg-gray-400 rounded-full"></span>
                <span>Přeskočeno ({{ props.skipped }})</span>
            </div>
            <div v-if="props.noMistakes > 0" class="flex items-center space-x-2">
                <span class="block w-3 h-3 md:w-4 md:h-4 bg-green-500 rounded-full"></span>
                <span>Bez chyby ({{ props.noMistakes }})</span>
            </div>
            <div v-if="props.oneMistake > 0" class="flex items-center space-x-2">
                <span class="block w-3 h-3 md:w-4 md:h-4 bg-yellow-400 rounded-full"></span>
                <span>Jedna chyba ({{ props.oneMistake }})</span>
            </div>
            <div v-if="props.twoMistakes > 0" class="flex items-center space-x-2">
                <span class="block w-3 h-3 md:w-4 md:h-4 bg-orange-400 rounded-full"></span>
                <span>Dvě chyby ({{ props.twoMistakes }})</span>
            </div>
            <div v-if="props.threeMistakes > 0" class="flex items-center space-x-2">
                <span class="block w-3 h-3 md:w-4 md:h-4 bg-red-500 rounded-full"></span>
                <span>Tři chyby ({{ props.threeMistakes }})</span>
            </div>
        </div>

        <div class="flex flex-col items-center my-8 md:my-12">
            <div class="flex justify-center text-center text-xl font-semibold mb-4">Jak se ti líbilo procvičování s touto aplikací?</div>
            <div class="flex space-x-3 md:space-x-6">
                <div v-for="(emoji, index) in emojiRatings" :key="index" class="flex flex-col items-center">
                    <button @click="selectedEmoji = index" :key="selectedEmoji"
                        class="text-5xl rounded-full transition transform hover:scale-110 border-4 p-2 text-gray-400 " :class="selectedEmoji === index
                            ? 'border-yellow-500 text-yellow-400 bg-yellow-100 shadow-md scale-110'
                            : 'border-gray-300 bg-white '">

                        <i :class="emoji.icon" class="drop-shadow-md bg-black p-1 rounded-full"></i>
                    </button>

                    <span class="text-center text-sm md:text-md font-medium mt-2 w-16 md:w-32">
                        {{ emoji.label }}
                    </span>
                </div>
            </div>
        </div>


        <div class="flex justify-center mt-12 md:mt-16 mb-6 w-full">
            <RouterLink to="/"
                @click="handleEmojiSelection"
                class="text-center text-xl md:text-3xl bg-secondary hover:bg-white text-white hover:text-secondary border-4 border-secondary rounded-xl font-semibold px-3 py-2 md:px-4 md:py-2 cursor-pointer transition">
                Zpět na hlavní stránku
            </RouterLink>
        </div>
    </div>
</template>
