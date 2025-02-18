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