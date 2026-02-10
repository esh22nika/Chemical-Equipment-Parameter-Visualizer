import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth Services
export const authService = {
  login: async (username, password) => {
    const response = await api.post('/auth/login/', { username, password });
    return response.data;
  },

  register: async (username, email, password) => {
    const response = await api.post('/auth/register/', { username, email, password });
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout/');
    return response.data;
  },
};

// Dataset Services
export const datasetService = {
  uploadCSV: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getDataset: async (datasetId) => {
    const response = await api.get(`/datasets/${datasetId}/`);
    return response.data;
  },

  getSummary: async (datasetId) => {
    const response = await api.get(`/summary/${datasetId}/`);
    return response.data;
  },

  getHistory: async () => {
    const response = await api.get('/history/');
    return response.data;
  },

  downloadPDF: async (datasetId) => {
    const response = await api.get(`/datasets/${datasetId}/download_pdf/`, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `report_${datasetId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },

  deleteDataset: async (datasetId) => {
    const response = await api.delete(`/datasets/${datasetId}/`);
    return response.data;
  },
};

export default api;
