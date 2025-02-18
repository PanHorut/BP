import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import HomeView from '@/views/HomeView.vue'
import TopicView from '@/views/TopicView.vue'
import ExampleView from '@/views/ExampleView.vue'
import SandboxView from '@/views/SandboxView.vue'
import TasksView from '@/views/TasksView.vue'
import SkillCreatorView from '@/views/SkillCreatorView.vue'
import ProfileView from '@/views/ProfileView.vue'
import AdminView from '@/views/AdminView.vue'
import RecordingView from '@/views/RecordingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },

    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
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
      meta: { requiresAdmin: true }
    },

    {
      path: '/tasks',
      name: 'tasks',
      component: TasksView,
      meta: { requiresAdmin: true }
    },

    {
      path: '/skill-creator',
      name: 'skill-creator',
      component: SkillCreatorView,
      meta: { requiresAdmin: true }
    },

    {
      path: '/transcript',
      name: 'transcript',
      component: RecordingView,
    },

    
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAdmin) {
    if (authStore.isAuthenticated && authStore.role === 'admin') {
      next(); 
    } else {
      next({ name: 'home' }); 
    }
  } else {
    next(); 
  }
});

export default router
