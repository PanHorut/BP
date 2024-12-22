import axios from 'axios';
import qs from 'qs'; 

const apiClient = axios.create({
  baseURL:  'https://bp-production-37c0.up.railway.app/api/', // 'http://localhost:8000/api/'
  headers: {
    'Content-Type': 'application/json',
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

export const postExamples = async (examples, selectedSkills, taskName) => {

    try {
      for (const example of examples.value) {
        const response = await apiClient.post('add-example/', {
          example: example.example, 
          answer: example.answer,
          input_type: example.input_type,         
          skill_ids: selectedSkills.map(skill => skill.id), 
          task_name: taskName
        });
        
        console.log('Example added:', response.data);
      }
      
      console.log('All examples added successfully!');
    } catch (error) {
      if (error.response) {
        console.error('Error adding example:', error.response.data);
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



export const getExamples = async (selectedIds) => {
  try {
    const response = await apiClient.get('examples/', {
      params: {
        skill_ids: selectedIds,
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

export default apiClient;