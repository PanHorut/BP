<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'
import { useLanguageStore } from '@/stores/useLanguageStore'
import { getSkillName } from '@/utils/dictionary'

const props = defineProps({
  topic: {
    type: String,
    required: true
  },
  id: {
    type: Number,
    required: true
  }
})

const router = useRouter()
const langStore = useLanguageStore()

function goToTopicDetail() {
  router.push({ name: 'topic', params: { id: Number(props.id) } })
}
</script>

<template>
  <div 
    @click="goToTopicDetail" 
    class="cursor-pointer border border-gray-300 rounded-lg shadow-lg max-w-md bg-white 
           transition transform  hover:shadow-xl 
           hover:bg-secondary hover:border-secondary"
  >
    <h2 class="flex justify-center text-3xl text-center font-bold text-primary p-4 
              transition duration-300 ease-in-out hover:text-white">
      {{ getSkillName(topic, langStore.language) }}
    </h2>
  </div>
</template>
