import axios from 'axios';

// Create a central Axios instance
const api = axios.create({
    // Adjust this URL to your backend's address and port
    baseURL: 'http://localhost:8000',
    timeout: 10000,
});

// Request Interceptor:
// This function will be called before every request is sent.
api.interceptors.request.use(
    (config) => {
        // Attempt to get the token from localStorage
        // The Pinia store will be responsible for placing it here upon login
        const token = localStorage.getItem('authToken');

        if (token) {
            // If the token exists, add it to the Authorization header
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Handle request error
        return Promise.reject(error);
    }
);

export default api;
