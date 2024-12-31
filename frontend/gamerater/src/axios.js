import axios from 'axios';
import router from '@/router';

const loadConfig = async () => {
    const response = await fetch('/config.json');
    return await response.json();
}
const config = await loadConfig();

const apiClient = axios.create({
  baseURL: config.API_URL,
  timeout: 10000,
  withCredentials: false,
});

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('Error response:', error.response);
    if (error.response && error.response.status === 403) {
      const customMessage = error.response.data.detail;
      if (customMessage === 'Account has not been activated') {
        router.push({ name: 'Login', query: { message: 'accountinactive' } });
      } else {
        router.push({ name: 'Login', query: { message: 'invalidtoken' } });
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;