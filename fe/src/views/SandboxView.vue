<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import SkillList from '@/components/TaskCreator/SkillList.vue';
import ExamplesList from '@/components/TaskCreator/ExamplesList.vue';
import LatexToolbar from '@/components/TaskCreator/LatexToolbar.vue';
import InputTypeSelector from '@/components/TaskCreator/InputTypeSelector.vue';

const selectedSkills = ref([]); 
const selectedInputType = ref('');
const taskName = ref('');
const examplesType = ref(null); 


const skillList = ref(null);

const updateSelectedSkills = (skills) => {
    selectedSkills.value = skills; 
};

const applyImport = (name, skills, form) => {
    taskName.value = name;
    
    selectedSkills.value = skills;
    skillList.value.importSkills(skills);
    examplesType.value = form;
    console.log(examplesType.value);
}

const clearInput = () => {
    taskName.value = ''; 
    skillList.value.clearSkills();
    
};

onMounted(() => {
    console.log(examplesType.value);
    examplesType.value = examplesType.value ?? 'classic';
});

</script>

<template>
    <div class="flex justify-center">
        <LatexToolbar v-if="examplesType == 'classic'"></LatexToolbar>
        <div class="flex justify-center flex-col items-center">
            <div class="flex w-full items-center my-2">
                <h2 class="text-2xl font-bold text-primary mr-8">Název cvičení:</h2>
                <input v-model="taskName" type="text" class="p-1 text-2xl border border-tertiary rounded-md">
            </div>

            <SkillList ref="skillList" @update-skills="updateSelectedSkills"></SkillList>
            <!--<InputTypeSelector v-model="selectedInputType"></InputTypeSelector>-->

            <div class="flex w-full justify-start items-center mt-4 space-x-8">
                <h1 class="text-primary font-bold text-2xl">Forma zadání:</h1>
                <label class="flex items-center space-x-2 cursor-pointer text-lg font-medium">
                    <input type="radio" v-model="examplesType" value="classic"
                        class="h-5 w-5 text-primary bg-transparent border-gray-500 checked:bg-primary checked:border-primary focus:ring-primary" />
                    <span class="text-primary text-2xl font-semibold">Klasické příklady</span>
                </label>
                <label class="flex items-center space-x-2 cursor-pointer text-lg font-medium">
                    <input type="radio" v-model="examplesType" value="word-problem"
                        class="h-5 w-5 text-primary bg-transparent border-gray-500 checked:bg-primary checked:border-primary focus:ring-primary" />
                    <span class="text-primary text-2xl font-semibold">Slovní úlohy</span>
                </label>
            </div>



            <ExamplesList :selectedSkills="selectedSkills" :inputType="selectedInputType" :taskName="taskName" :examplesType="examplesType"
                @importTask="applyImport" @submit="clearInput"></ExamplesList>
        </div>
    </div>
</template>
