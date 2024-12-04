import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/',
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

export default apiClient;