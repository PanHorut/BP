/**
 * ================================================================================
 * File: useMainpageTopicStore.js
 * Description:
 *       Pinia store for managing the topics (skills) on the landing page, including fetching and caching the data.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

import { defineStore } from 'pinia';
import { getLandingPageSkills } from '@/api/apiClient';

export const useTopicStore = defineStore('topicStore', {
  
  state: () => ({
    topics: [],
    loading: false,
    lastFetched: null
  }),

  actions: {
    async fetchTopics(forceRefresh = false) {
      const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes
      const now = new Date().getTime();

      // Check if the cache is still valid
      if (!forceRefresh && this.lastFetched && now - this.lastFetched < CACHE_DURATION) {
        return;
      }

      this.loading = true;

      try {
        // Fetch data from the API and update the state
        const data = await getLandingPageSkills();
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
