/**
 * ================================================================================
 * File: useTaskStore.js
 * Description:
 *       Pinia store to share task data across unrelated components.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

import { defineStore } from 'pinia';

export const useTaskStore = defineStore('taskStore', {
  state: () => ({
    task: null,
    skills: [],
    
  }),
  actions: {
    setTask(task, skills) {
      this.task = task;
      this.skills = skills;
    }
  }
});