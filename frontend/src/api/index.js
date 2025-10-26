import axios from 'axios';

// 1. Create axios instance
const apiClient = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// 2. Implement request interceptor for JWT
apiClient.interceptors.request.use(
    (config) => {
        // Get token from localStorage (or Pinia store)
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 3. Export API functions

/**
 * Handles user login.
 * Note: FastAPI's OAuth2PasswordRequestForm expects form data.
 * @param {object} credentials - {username, password}
 * @returns {Promise} Axios response
 */
export const login = (credentials) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    return apiClient.post('/auth/token', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
};

/**
 * Fetches a list of all campaigns.
 * Corresponds to CampaignRead schema.
 * @returns {Promise} Axios response
 */
export const getCampaigns = () => {
    return apiClient.get('/campaigns');
};

/**
 * Fetches a single campaign by its ID.
 * Corresponds to CampaignRead schema.
 * @param {number} id - The campaign ID
 * @returns {Promise} Axios response
 */
export const getCampaign = (id) => {
    return apiClient.get(`/campaigns/${id}`);
};

/**
 * Creates a new campaign.
 * @param {object} data - Campaign data (conforms to CampaignCreate schema)
 * @returns {Promise} Axios response
 */
export const createCampaign = (data) => {
    // Data should match schemas.CampaignCreate
    // { name: string, description?: string, start_date: date, end_date: date, budget: float, kpis: object }
    return apiClient.post('/campaigns', data);
};

/**
 * Updates an existing campaign.
 * @param {number} id - The campaign ID
 * @param {object} data - Campaign data (conforms to CampaignUpdate schema)
 * @returns {Promise} Axios response
 */
export const updateCampaign = (id, data) => {
    // Data should match schemas.CampaignUpdate
    // { name?: string, description?: string, end_date?: date, budget?: float, kpis?: object }
    return apiClient.put(`/campaigns/${id}`, data);
};

/**
 * Deletes a campaign by its ID.
 * @param {number} id - The campaign ID
 * @returns {Promise} Axios response
 */
export const deleteCampaign = (id) => {
    return apiClient.delete(`/campaigns/${id}`);
};

/**
 * Toggles the 'is_active' status of a campaign.
 * We use PATCH for this partial update.
 * @param {number} id - The campaign ID
 * @returns {Promise} Axios response
 */
export const toggleCampaignStatus = (id) => {
    // This assumes the backend has a PATCH endpoint to update 'is_active'
    // Alternatively, if the endpoint is specific (e.g., POST /campaigns/{id}/toggle)
    // this function should be changed.
    // We'll assume a PATCH request to the main endpoint.
    // The backend logic will handle the toggle.
    return apiClient.patch(`/campaigns/${id}/toggle_status`);
};

// Export default object with all API functions
export default {
    login,
    getCampaigns,
    getCampaign,
    createCampaign,
    updateCampaign,
    deleteCampaign,
    toggleCampaignStatus
};
