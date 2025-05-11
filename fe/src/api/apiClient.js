/**
 * ================================================================================
 * File: apiClient.js
 * Description:
 *       Axios client setup and API utility functions for interacting with the server.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

import axios from 'axios';
import qs from 'qs'; 

// Axios instance for all API requests
const apiClient = axios.create({
  baseURL:   'http://localhost:8000/api/',// 'https://bp-production-37c0.up.railway.app/api/',    'https://drillovacka.applikuapp.com/api/'
  headers: {
  },
});

/**
 * Creates a new record indicating that a student has practiced a example.
 * 
 * @param {number} studentId - id of the student.
 * @param {number} exampleId - id of the example.
 * @returns {string} timestamp of record.
 */
export const createRecord = async (studentId, exampleId) => {
    try {
      const response = await apiClient.post('create-record/', {
        student_id: studentId,
        example_id: exampleId,
      });

      return response.data; 
    } catch (error) {

      throw error.response?.data?.error || 'Error creating record.';
    }
};

/**
 * Deletes a record that student practiced example.
 * 
 * @param {number} studentId - id of the student.
 * @param {number} exampleId - id of the example.
 * @param {string} date - timestamp of record creation.
 */
export const deleteRecord = async (studentId, exampleId, date) => {
  try {
    await apiClient.post('delete-record/', {
      student_id: studentId,
      example_id: exampleId,
      date
    });
  } catch (error) {
    throw error.response?.data?.error || 'Error updating record.';
  }
};

/**
 * Marks an example as skipped in record.
 * 
 * @param {number} studentId - id of the student.
 * @param {number} exampleId - id of the example.
 * @param {string} date - timestamp of record creation.
 */
export const skipExample = async (studentId, exampleId, date) => {
  try {
    await apiClient.post('skip-example/', {
      student_id: studentId,
      example_id: exampleId,
      date,
    });

  }catch (error) {
      throw error.response?.data?.error || 'Error skipping example.';
    }
};

/**
 * Creates or updates a task along with its associated examples.
 * 
 * @param {Array<Object>} examples - list of examples.
 * @param {Array<Object>} selectedSkills - list of selected skills.
 * @param {string} taskName - name of the task.
 * @param {number} taskId - id of the task (null if creating a new one).
 * @param {string} taskForm - form of task examples (classic or word-problem).
 * @param {string} action action type ('create' or 'update').
 */
export const postTask = async (examples, selectedSkills, taskName, taskId, taskForm, action) => {
  try {
      const payload = {
          task_name: taskName,
          task_id: taskId,
          task_form: taskForm,  
          skill_ids: selectedSkills.map(skill => skill.id),
          examples: examples.value.map(example => ({
              example: example.example,
              example_id: example.example_id,
              answer: example.answer,
              input_type: example.input_type,
              steps: example.steps,
          }))
      };

      await apiClient.post(`${action}-task/`, payload);

  } catch (error) {
      if (error.response) {
          console.error('Error adding examples:', error.response.data);
      } else {
          console.error('Network or server error:', error.message);
      }
  }
};

/**
 * Gets skill data by its id.
 * 
 * @param {number} id - id of the skill.
 * @returns {Promise<Object>} skill data.
 */
export const getSkill = async (id) => {
  try {
    const response = await apiClient.get(`skill/${id}/`);
    return response.data;
    
  } catch (error) {
    console.error("Error fetching skill:", error)
  }
};

/**
 * Fetches a list of examples based on the provided skill ids.
 * 
 * @param {Array<string|number>} topics - array of skill or topic identifiers.
 * @returns {Promise<Array<Object>>} list of example objects.
 */
export const getExamples = async (topics) => {
  try {
    const response = await apiClient.get('examples/', {
      params: {
        topics: JSON.stringify(topics),
      },
      paramsSerializer: (params) => {
        return qs.stringify(params, { arrayFormat: 'repeat' });
      },
    });

    return response.data;

  } catch (error) {
    console.error("Error fetching examples:", error);
  }
};

/**
 * Retrieves all tasks.
 * 
 * @returns {Promise<Array<Object>>} array of task objects.
 */
export const getTasks = async () => {
  try {
    const response = await apiClient.get('tasks/'); 
    return response.data;
    
  } catch (error) {
    console.error("Error fetching skills:", error)
  }
};

/**
 * Deletes an example by its id.
 * 
 * @param {number} exampleId - id of the example.
 */
export const deleteExample = async (exampleId) => {
  try {
    await apiClient.delete(`example/${exampleId}/delete/`);

  } catch (error) {
    throw error.response?.data?.error || 'Error deleting example.';
  }
};

/**
 * Deletes a task and its associated examples.
 * 
 * @param {number} taskId - id of the task.
 */
export const deleteTask = async (taskId) => {
  try {
    await apiClient.delete(`tasks/${taskId}/delete/`);

  } catch (error) {
    console.error('Error deleting task:', error);
  }
};

/**
 * Creates a new skill or recreates a previously soft-deleted one.
 * 
 * @param {string} name - name of the skill to be created.
 * @param {number} [parent_id=null] - id of the parent skill, if any.
 * @returns {Promise<Object>} created skill data.
 */
export const createSkill = async (name, parent_id = null) => {
  try {
    const response = await apiClient.post('create-skill/', {
      name,
      parent_skill: parent_id, 
    });

    return response.data; 

  } catch (error) {
    throw error.response?.data?.error || 'Error creating skill.';
  }
};

/**
 * Retrieves the full skill tree.
 * 
 * @returns {Promise<Array<Object>>} array representing the skill tree structure.
 */
export const getSkillTree = async () => {
  try {
    const response = await apiClient.get('skill-tree/');

    return response.data;

  } catch (error) {
    console.error('Error fetching skill tree:', error);
  }
};

/**
 * Searches for child skills based on a query and a parent skill ID.
 * 
 * @param {string} query - search keyword to filter skills.
 * @param {number} skillId - id of the parent skill.
 * @returns {Promise<Array<Object>>} list of matching skills.
 */
export const searchSkills = async (query, skillId) => {
  console.log(typeof(skillId))
  try {
    const response = await apiClient.get('skills/search/', {
      params: {
        q: query,
        skill_id: skillId
      }
    });

    return response.data;

  } catch (error) {
    console.error('Error fetching search results:', error);
    return [];
  }
};

/**
 * Retrieves a list of skills to be shown on the landing page.
 * 
 * @returns {Promise<Array<Object>>} - array of landing page skills.
 */
export const getLandingPageSkills = async () => {
  try {
    const response = await apiClient.get('landing-page-skills/');

    return response.data;

  } catch (error) {
    console.error('Error fetching landing page skills:', error);
  }
};

/**
 * Retrieves the related skills tree for a given skill id.
 * 
 * @param {number} skillId - id of the skill to fetch related skills for.
 * @returns {Promise<Object>} related skills tree.
 */
export const getRelatedSkillsTree = async (skillId) => {
  try {
    const response = await apiClient.get(`skills/${skillId}/tree/related`);

    return response.data;

  } catch (error) {
    console.error('Error fetching related skills:', error);
  }
};

/**
 * Retrieves the children skills tree for a given skill ID.
 * 
 * @param {number} skillId - id of the parent skill.
 * @param {boolean} withCounts whether to include counts of examples.
 * @returns {Promise<Object>} children skills tree.
 */
export const getChildrenSkillsTree = async (skillId, withCounts) => {
  try {
    const response = await apiClient.get(`skills/${skillId}/tree/children`,{
      params: {
        with_counts: withCounts,
      }
    });

    return response.data;

  } catch (error) {
    console.error('Error fetching related skills:', error);
  }
};

/**
 * Retrieves operation skills associated with a specific skill ID.
 * 
 * @param {number} skillId - id of the skill to fetch operation skills for.
 * @returns {Promise<Array<Object>>} list of operation skills.
 */
export const getOperationSkills = async (skillId) => {
  try {
    const response = await apiClient.get(`skills/${skillId}/operations`);

    return response.data;

  } catch (error) {
    console.error('Error fetching operation skills:', error);
  }
};

/**
 * Soft-deletes a skill by its id.
 * 
 * @param {number} skillId - id of the skill to be deleted.
 */
export const deleteSkill = async (skillId) => {
  try {
    await apiClient.patch(`skills/${skillId}/delete/`);

  } catch (error) {
    throw error.response?.data?.error || 'Error deleting skill';
  }
};

/**
 * Registers a new user with the provided username and passphrase.
 * 
 * @param {string} username - username for the new user.
 * @param {string} passphrase - passphrase for the new user.
 * @returns {Promise<Object>} server response..
 */
export const registerStudent = async (username, passphrase) => {
  try {
    const response = await apiClient.post('/register/student', {
      username,
      passphrase
    });

    return response;

  } catch (error) {

    if (error.response && error.response.data) {
      return { error: error.response.data.error };
    }
  }
};

/**
 * Logs in a user using the provided credentials.
 * 
 * @param {string} username - users username.
 * @param {string} passphrase - users passphrase.
 * @returns {Promise<Object>} server response.
 */
export const loginStudent = async (username, passphrase) => {
  try {
    const response = await apiClient.post('/login/student', {
      username,
      passphrase
    });

    return response;

  } catch (error) {
    if (error.response && error.response.data) {
      return { error: error.response.data.error };
    }
  }
};

/**
 * Logs in an admin using the provided credentials.
 * 
 * @param {string} username - The admin's username.
 * @param {string} password - The admin's password.
 * @returns {Promise<Object>} the server.
 */
export const loginAdmin = async (username, password) => {
  try {
    const response = await apiClient.post('/login/admin', {
      username,
      password
    });

    return response;

  } catch (error) {
    if (error.response && error.response.data) {
      return { error: error.response.data.error };
    }
  }
};

/**
 * Checks whether the users answer to an example is correct and returns evaluation data.
 * 
 * @param {number} student_id - id of the user.
 * @param {number} example_id - id of the example.
 * @param {string} date - timestamp of record.
 * @param {number} duration - elapsed time user practiced example.
 * @param {string} student_answer - users answer.
 * @param {string} answer_type - type of answer type ('inline', 'frac', 'var').
 * @returns {Promise<Object>} evaluation result from the server.
 */
export const checkAnswer = async (student_id, example_id, date, duration, student_answer, answer_type) => {
  try {
    const response = await apiClient.post('check-answer/', {
      student_id,
      example_id,
      date,
      duration,
      student_answer,
      answer_type
    });

    return response.data;

  } catch (error) {
    console.error('Error checking answer:', error);
  }
};

/**
 * Retrieves full skill paths for the given skill ids, returning the paths with entire skill data.
 * 
 * @param {Array<number>} skillIds - array of skill ids to retrieve paths for.
 * @returns {Promise<Object>} skill paths.
 */
export const getSandboxSkillPaths = async (skillIds) => {
  try {
    const response = await apiClient.get('skills/paths/sandbox/', {
      params: {
        skill_ids: skillIds
      },
      paramsSerializer: (params) => {
        return new URLSearchParams(params).toString();
      }
    });

    return response.data;

  } catch (error) {
    console.error('Error fetching sandbox skill paths:', error);
  }
};

/**
 * Retrieves the number of tasks and examples associated with a given skill id.
 * 
 * @param {number} skillId - id of the skill to fetch related task and example counts for.
 * @returns {Promise<Object>} counts of related tasks and examples.
 */
export const getRelatedTasksCount = async (skillId) => {
  try {
    const response = await apiClient.get('skills/related-counts/', {
      params: {
        skill_id: skillId
      }
    });

    return response.data;

  } catch (error) {
    console.error('Error fetching tasks and examples count:', error);
  }
};

/**
 * Submits an answer to a survey question, along with optional related skills.
 * 
 * @param {string} questionType - category of the survey question.
 * @param {string} questionText - text of the survey question.
 * @param {string} answer - users answer to the question.
 * @param {Array<number>} skills - array of skill ids which user was practicing.
 */
export const sendSurveyAnswer = async (questionType, questionText, answer, skills) => {
  try {
    await apiClient.post('survey-answer/', {
      question_type: questionType,
      question_text: questionText,
      answer,
      skills
    });

  } catch (error) {
    console.error('Error sending survey answer:', error);
  }
};

export default apiClient;
