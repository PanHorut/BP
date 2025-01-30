import { defineStore } from 'pinia';
import { getParentSkills } from '@/api/apiClient';

export const useTopicStore = defineStore('topicStore', {
  state: () => ({
    topics: [],
    loading: false,
    lastFetched: null
  }),

  actions: {
    async fetchTopics(forceRefresh = false) {
      const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
      const now = new Date().getTime();

      if (!forceRefresh && this.lastFetched && now - this.lastFetched < CACHE_DURATION) {
        return;
      }

      this.loading = true;
      try {
        const data = await getParentSkills();
        this.topics = data;
        this.lastFetched = now;
      } catch (error) {
        console.error('Failed to fetch topics:', error);
      } finally {
        this.loading = false;
      }
    }
  }
});
