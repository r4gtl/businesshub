import axios from 'axios';
import type { AxiosRequestConfig } from 'axios';

const baseURL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const instance = axios.create({
  baseURL,
  withCredentials: true, // solo se usi cookie, altrimenti puoi rimuoverlo
});

// Interceptor: aggiunge Authorization header se il token è presente
instance.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = localStorage.getItem('accessToken');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor: gestisce refresh automatico del token
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refreshToken')
    ) {
      originalRequest._retry = true;
      try {
        const refreshResponse = await axios.post(`${baseURL}/token/refresh/`, {
          refresh: localStorage.getItem('refreshToken'),
        });

        const newAccessToken = refreshResponse.data.access;
        localStorage.setItem('accessToken', newAccessToken);

        if (originalRequest.headers)
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return instance(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default instance;
