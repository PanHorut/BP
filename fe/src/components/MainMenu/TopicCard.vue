<script setup>
import {ref, computed } from 'vue';
import { RouterLink, useRoute } from 'vue-router';


import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

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

function goToTopicDetail() {
  router.push({ name: 'topic', params: { id: props.id } })
}
</script>

<template>
    <div @click="goToTopicDetail" class="cursor-pointer border border-gray-300 rounded-lg shadow-lg max-w-md bg-white">

        <h2 class="flex justify-center text-2xl text-center font-bold text-gray-800 p-4">
           {{ topic }}
        </h2>
        
    </div>

</template>