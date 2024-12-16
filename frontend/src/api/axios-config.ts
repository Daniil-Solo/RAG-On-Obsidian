import axios from 'axios';


const MODE = import.meta.env.VITE_APPLICATION_MODE;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const axiosInstance = axios.create({
    baseURL: MODE === "dev"? API_BASE_URL: undefined,
    withCredentials: false,
});

axiosInstance.defaults.headers.common['Content-Type'] = 'application/json';

export default axiosInstance;