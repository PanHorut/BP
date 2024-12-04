<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import SkillList from '@/components/TaskCreator/SkillList.vue';
import ExamplesList from '@/components/TaskCreator/ExamplesList.vue';
import LatexToolbar from '@/components/TaskCreator/LatexToolbar.vue';
import InputTypeSelector from '@/components/TaskCreator/InputTypeSelector.vue';

const selectedSkills = ref([]); 
const selectedInputType = ref('');
const taskName = ref('');

const skillList = ref(null);

const updateSelectedSkills = (skills) => {
    selectedSkills.value = skills; 
};

const applyImport = (name, skills) => {
    taskName.value = name;
    
    selectedSkills.value = skills;
    skillList.value.importSkills(skills);
}

</script>

<template>
    <div class="flex justify-center">
        <LatexToolbar></LatexToolbar>
        <div class="flex justify-center flex-col items-center">
        <div class="flex w-full items-center my-2">
            <h2 class="text-2xl font-bold text-primary mr-2">Název cvičení:</h2>
            <input v-model="taskName" type="text" class="p-1 text-2xl border border-tertiary">
        </div>    
        <SkillList ref="skillList" @update-skills="updateSelectedSkills"></SkillList>
        <InputTypeSelector 
            v-model="selectedInputType">
        </InputTypeSelector>
        <ExamplesList :selectedSkills="selectedSkills" :inputType="selectedInputType" :taskName="taskName" @importTask="applyImport"></ExamplesList>
        </div>
    </div>
</template>
