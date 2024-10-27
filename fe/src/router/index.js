import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import TopicView from '@/views/TopicView.vue'
import ExampleView from '@/views/ExampleView.vue'
import SandboxView from '@/views/SandboxView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/topics',
      name: 'topic',
      component: TopicView,
    },

    {
      path: '/examples',
      name: 'example',
      component: ExampleView,
    },

    {
      path: '/sandbox',
      name: 'sandbox',
      component: SandboxView,
    },
  ]
})

export default router
