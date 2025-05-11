import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

// Import views
import HomeView from '@/views/HomeView.vue'
import TopicView from '@/views/TopicView.vue'
import ExampleView from '@/views/ExampleView.vue'
import SandboxView from '@/views/SandboxView.vue'
import TasksView from '@/views/TasksView.vue'
import SkillCreatorView from '@/views/SkillCreatorView.vue'
import ProfileView from '@/views/ProfileView.vue'
import AdminView from '@/views/AdminView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { lang: 'cs' }

    },
    {
      path: '/en',
      name: 'home-en',
      component: HomeView,
      meta: { lang: 'en' }
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
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  // If the route requires admin access
  if (to.meta.requiresAdmin) {
    if (authStore.isAuthenticated && authStore.role === 'admin') {
      // Authenticated as admin - allow
      next(); 

    } else {
      // Not authenticated as admin - redirect to home
      next({ name: 'home' }); 
    }
  } else {
    next(); 
  }
});

export default router
