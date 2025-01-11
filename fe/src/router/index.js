import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import TopicView from '@/views/TopicView.vue'
import ExampleView from '@/views/ExampleView.vue'
import SandboxView from '@/views/SandboxView.vue'
import TasksView from '@/views/TasksView.vue'
import SkillCreatorView from '@/views/SkillCreatorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/topic/:id',
      name: 'topic',
      component: TopicView,
      props: true
    },

    {
      path: '/examples',
      name: 'examples',
      component: ExampleView,
      props: true
    },

    {
      path: '/sandbox',
      name: 'sandbox',
      component: SandboxView,
    },

    {
      path: '/tasks',
      name: 'tasks',
      component: TasksView,
    },

    {
      path: '/skill-creator',
      name: 'skill-creato',
      component: SkillCreatorView,
    },
  ]
})

export default router
