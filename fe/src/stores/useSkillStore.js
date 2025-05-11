/**
 * ================================================================================
 * File: useSkillStore.js
 * Description:
 *       Pinia store for managing skill data, including fetching skills and caching them.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

import { defineStore } from 'pinia';
import { getSkill, getRelatedSkillsTree, getChildrenSkillsTree, getOperationSkills } from '@/api/apiClient';

export const useSkillStore = defineStore('skills', {
  state: () => ({
    skills: {},
    relatedSkillsTrees: {},
    childrenSkillsTrees: {},
    operationSkills: {},
    cacheTimestamp: {},
    cacheExpiry: 30 * 60 * 1000, // 30 minutes cache
  }),

  actions: {
    async fetchSkill(id) {
      const now = Date.now();
      const cacheKey = `skill-${id}`;

      // Return cached skill if it exists and has not expired
      if (this.skills[id] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        return this.skills[id];
      }

      // No cached skill, fetch from API and cache it
      const skill = await getSkill(id);
      this.skills[id] = skill;
      this.cacheTimestamp[cacheKey] = now;

      return skill;
    },

    async fetchRelatedSkillsTree(id) {
      const now = Date.now();
      const cacheKey = `related-${id}`;

      // Return cached related skills tree if it exists and is still valid
      if (this.relatedSkillsTrees[id] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        return this.relatedSkillsTrees[id];
      }

      // No cached skill, fetch from API and cache it
      const tree = await getRelatedSkillsTree(id);
      this.relatedSkillsTrees[id] = tree;
      this.cacheTimestamp[cacheKey] = now;

      return tree;
    },

    async fetchChildrenSkillsTree(id, includeEquations) {
      const now = Date.now();
      const cacheKey = `children-${id}-${includeEquations}`;

      // Return cached children skills tree if it exists and is still valid
      if (this.childrenSkillsTrees[cacheKey] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        // Clear the 'examples' count field for each item in the tree  
        this.childrenSkillsTrees[cacheKey].forEach(item => {
          item.examples = 0;
        });
        return this.childrenSkillsTrees[cacheKey];
      }

      // No cached skill, fetch from API and cache it
      const tree = await getChildrenSkillsTree(id, includeEquations);
      this.childrenSkillsTrees[cacheKey] = tree;
      this.cacheTimestamp[cacheKey] = now;

      return tree;
    },

    async fetchOperationSkills(id) {
      const now = Date.now();
      const cacheKey = `operations-${id}`;

      // Return cached children skills tree if it exists and is still valid
      if (this.operationSkills[id] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        return this.operationSkills[id];
      }

      // No cached skill, fetch from API and cache it
      const operations = await getOperationSkills(id);
      this.operationSkills[id] = operations;
      this.cacheTimestamp[cacheKey] = now;

      return operations;
    },

    clearCache() {
      this.skills = {};
      this.relatedSkillsTrees = {};
      this.childrenSkillsTrees = {};
      this.operationSkills = {};
      this.cacheTimestamp = {};
    }
  }
});