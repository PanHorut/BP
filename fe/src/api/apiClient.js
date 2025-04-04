import axios from 'axios';
import qs from 'qs'; 

const apiClient = axios.create({
  baseURL:  'https://drillovacka.applikuapp.com/api/',// 'https://bp-production-37c0.up.railway.app/api/',    'http://localhost:8000/api/'
  headers: {
    //'Content-Type': 'application/json',
  },
});

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

export const updateRecord = async (studentId, exampleId, isCorrect, time, date) => {
    try {
      const response = await apiClient.post('update-record/', {
        student_id: studentId,
        example_id: exampleId,
        isCorrect,
        time,
        date,
        
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.error || 'Error updating record.';
    }
};

export const deleteRecord = async (studentId, exampleId, date) => {

  try {
    const response = await apiClient.post('delete-record/', {
      student_id: studentId,
      example_id: exampleId,
      date
      });
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Error updating record.';
  }

}

export const skipExample = async (studentId, exampleId, date) => {
  try {
    const response = await apiClient.post('skip-example/', {
      student_id: studentId,
      example_id: exampleId,
      date,
      
    });
    return response.data;
  }catch (error) {
      throw error.response?.data?.error || 'Error skipping example.';
    }
}

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

      const response = await apiClient.post(`${action}-task/`, payload);

      console.log('Examples added successfully:', response.data);
  } catch (error) {
      if (error.response) {
          console.error('Error adding examples:', error.response.data);
      } else {
          console.error('Network or server error:', error.message);
      }
  }
};

export const getParentSkills = async () => {
  try {
    const response = await apiClient.get('parent-skills/');
    return response.data
  
  } catch (error) {
    console.error("Error fetching skills:", error)
  }

}

export const getSkill = async (id) => {
  try {
    const response = await apiClient.get(`skill/${id}/`);
    return response.data;
    
  } catch (error) {
    console.error("Error fetching skill:", error)
  }
}

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

export const getLeafSkills = async () => {
  try {
    const response = await apiClient.get('leaf-skills/'); 
    return response.data;
    
  } catch (error) {
    console.error("Error fetching skills:", error)
  }
}

export const getTasks = async () => {
  try {
    const response = await apiClient.get('tasks/'); 
    return response.data;
    
  } catch (error) {
    console.error("Error fetching skills:", error)
  }
}

export const deleteExample = async (exampleId) => {
  try {
    const response = await apiClient.delete(`example/${exampleId}/delete/`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Error deleting example.';
  }
};

export const deleteTask = async (taskId) => {
  try {
    const response = await apiClient.delete(`tasks/${taskId}/delete/`);
    console.log('Task deleted successfully');
  } catch (error) {
    console.error('Error deleting task:', error);
  }
};

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

export const getSkillTree = async () => {
  try {
    const response = await apiClient.get('skill-tree/');
    return response.data;
  } catch (error) {
    console.error('Error fetching skill tree:', error);
  }
};

export const searchSkills = async (query, skillId) => {
  try {
    // Send both query and parent_skill_id in the API request
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
}



export const getLandingPageSkills = async () => {
  try {
    const response = await apiClient.get('landing-page-skills/');
    return response.data;
  } catch (error) {
    console.error('Error fetching landing page skills:', error);
  }
}

export const getRelatedSkillsTree = async (skillId) => {
  try {
    const response = await apiClient.get(`skills/${skillId}/tree/related`);
    return response.data;
  } catch (error) {
    console.error('Error fetching related skills:', error);
  }
}

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
}

export const getOperationSkills = async (skillId) => {
  try {
    const response = await apiClient.get(`skills/${skillId}/operations`);
    return response.data;
  } catch (error) {
    console.error('Error fetching operation skills:', error);
  }
}

export const deleteSkill = async (skillId) => {
  try {
    const response = await apiClient.patch(`skills/${skillId}/delete/`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Error deleting skill';
  }
};

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
}

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
}

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
}

export const sendSurveyAnswer = async (questionType, questionText, answer, skills) => {
  try {
    const response = await apiClient.post('survey-answer/', {
      question_type: questionType,
      question_text: questionText,
      answer,
      skills

    });
  } catch (error) {
    console.error('Error sending survey answer:', error);
  }
}

export default apiClient;
