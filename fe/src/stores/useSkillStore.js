import { defineStore } from 'pinia';
import { getSkill, getRelatedSkillsTree, getChildrenSkillsTree, getOperationSkills } from '@/api/apiClient';

export const useSkillStore = defineStore('skills', {
  state: () => ({
    skills: {},
    relatedSkillsTrees: {},
    childrenSkillsTrees: {},
    operationSkills: {},
    cacheTimestamp: {},
    cacheExpiry: 60 * 60 * 1000, // 60 minutes
  }),

  actions: {
    async fetchSkill(id) {
      const now = Date.now();
      const cacheKey = `skill-${id}`;

      if (this.skills[id] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        return this.skills[id];
      }

      const skill = await getSkill(id);

      this.skills[id] = skill;
      this.cacheTimestamp[cacheKey] = now;

      return skill;
    },

    async fetchRelatedSkillsTree(id) {
      const now = Date.now();
      const cacheKey = `related-${id}`;

      if (this.relatedSkillsTrees[id] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        return this.relatedSkillsTrees[id];
      }

      const tree = await getRelatedSkillsTree(id);
      this.relatedSkillsTrees[id] = tree;
      this.cacheTimestamp[cacheKey] = now;

      return tree;
    },

    async fetchChildrenSkillsTree(id, includeEquations) {
      const now = Date.now();
      const cacheKey = `children-${id}-${includeEquations}`;

      if (this.childrenSkillsTrees[cacheKey] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        this.childrenSkillsTrees[cacheKey].forEach(item => {
          item.examples = 0;
        });
        return this.childrenSkillsTrees[cacheKey];
      }

      const tree = await getChildrenSkillsTree(id, includeEquations);
      this.childrenSkillsTrees[cacheKey] = tree;
      this.cacheTimestamp[cacheKey] = now;

      return tree;
    },

    async fetchOperationSkills(id) {
      const now = Date.now();
      const cacheKey = `operations-${id}`;

      if (this.operationSkills[id] && this.cacheTimestamp[cacheKey] &&
        (now - this.cacheTimestamp[cacheKey]) < this.cacheExpiry) {
        return this.operationSkills[id];
      }

      const operations = await getOperationSkills(id);
      this.operationSkills[id] = operations;
      this.cacheTimestamp[cacheKey] = now;

      return operations;
    },

    // Optional: method to clear cache
    clearCache() {
      this.skills = {};
      this.relatedSkillsTrees = {};
      this.childrenSkillsTrees = {};
      this.operationSkills = {};
      this.cacheTimestamp = {};
    }
  }
});