import axios from 'axios';


const MODE = import.meta.env.VITE_APPLICATION_MODE;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const axiosInstance = axios.create({
    baseURL: MODE === "dev"? API_BASE_URL: undefined,
    withCredentials: false,
});

axiosInstance.defaults.headers.common['Content-Type'] = 'application/json';

axiosInstance.interceptors.request.use(
    config => {
        const auth_token = localStorage.getItem(AUTH_TOKEN_KEY);
        if (auth_token != null){
            config.headers['Authorization'] = `Bearer ${auth_token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export default axiosInstance;