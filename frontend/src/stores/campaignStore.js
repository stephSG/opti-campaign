import { defineStore } from 'pinia';
import api from '../api'; // Import our configured Axios instance

export const useCampaignStore = defineStore('campaign', {
    /**
     * State definition:
     * token: Initialized from localStorage to persist login session
     * campaigns: List of all campaigns
     * isLoading/error: For UI state management
     */
    state: () => ({
        campaigns: [],
        isLoading: false,
        error: null,
        token: localStorage.getItem('authToken') || null,
    }),

    /**
     * Getters: Computed properties derived from state
     */
    getters: {
        isAuthenticated: (state) => !!state.token,
    },

    /**
     * Actions: Methods that perform asynchronous operations
     */
    actions: {
        /**
         * Authenticates a user, stores the token, and updates API headers.
         * FastAPI's default OAuth2 expects form data.
         */
        async login(username, password) {
            this.isLoading = true;
            this.error = null;
            try {
                const formData = new URLSearchParams();
                formData.append('username', username);
                formData.append('password', password);

                const response = await api.post('/auth/token', formData, {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                });

                const token = response.data.access_token;
                this.token = token;
                localStorage.setItem('authToken', token);

                // Set the default auth header for all subsequent API requests
                api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            } catch (err) {
                this.error = err.response?.data?.detail || 'Failed to login';
                throw err; // Re-throw to let the component handle it (e.g., show error)
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Logs the user out by clearing the token from state and localStorage.
         */
        logout() {
            this.token = null;
            localStorage.removeItem('authToken');
            // Remove the default auth header
            delete api.defaults.headers.common['Authorization'];
        },

        /**
         * Fetches all campaigns from the backend.
         */
        async fetchCampaigns() {
            this.isLoading = true;
            this.error = null;
            try {
                const response = await api.get('/campaigns/');
                this.campaigns = response.data;
            } catch (err) {
                this.error = 'Failed to fetch campaigns';
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Creates a new campaign.
         */
        async createCampaign(campaignData) {
            this.isLoading = true;
            this.error = null;
            try {
                const response = await api.post('/campaigns/', campaignData);
                // Add the new campaign to the local state
                this.campaigns.push(response.data);
            } catch (err) {
                this.error = 'Failed to create campaign';
                throw err;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Updates an existing campaign by its ID.
         */
        async updateCampaign(id, campaignData) {
            this.isLoading = true;
            this.error = null;
            try {
                const response = await api.put(`/campaigns/${id}`, campaignData);
                // Find and update the campaign in the local state
                const index = this.campaigns.findIndex((c) => c.id === id);
                if (index !== -1) {
                    this.campaigns[index] = response.data;
                }
            } catch (err) {
                this.error = 'Failed to update campaign';
                throw err;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Deletes a campaign by its ID.
         */
        async deleteCampaign(id) {
            this.isLoading = true;
            this.error = null;
            try {
                await api.delete(`/campaigns/${id}`);
                // Remove the campaign from the local state
                this.campaigns = this.campaigns.filter((c) => c.id !== id);
            } catch (err) {
                this.error = 'Failed to delete campaign';
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Toggles the 'status' (active/inactive) of a campaign.
         * This re-uses the updateCampaign action.
         */
        async toggleCampaign(id) {
            const campaign = this.campaigns.find((c) => c.id === id);
            if (!campaign) {
                this.error = 'Campaign not found';
                return;
            }
            // Create a payload with the toggled status
            const updatedData = { ...campaign, status: !campaign.status };

            // We only send the fields the update schema expects (pydantic model)
            // This assumes the backend model matches the frontend object.
            // Adjust if the backend expects a partial DTO (e.g., CampaignUpdate schema)
            await this.updateCampaign(id, updatedData);
        },
    },
});
