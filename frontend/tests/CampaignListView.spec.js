import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { nextTick } from 'vue';
import CampaignListView from '../src/views/CampaignListView.vue';

// --- Mocking Strategy ---
let mockStoreState = {};

vi.mock('../src/stores/campaignStore', () => ({
  useCampaignStore: () => ({
    campaigns: [],
    isLoading: false,
    error: null,
    ...mockStoreState,
    fetchCampaigns: vi.fn(),
    deleteCampaign: vi.fn(),
    toggleCampaign: vi.fn(),
  }),
}));

describe('CampaignListView.vue', () => {

  beforeEach(() => {
    vi.clearAllMocks();
    mockStoreState = {};
  });

  /**
   * Test: Loading State
   * Description: Verifies the component shows a loading indicator when `isLoading` is true.
   */
  it('should show a loading message when isLoading is true', async () => {
    mockStoreState = { isLoading: true };
    const wrapper = mount(CampaignListView, { global: { stubs: { 'router-link': true } } });
    await nextTick();
    expect(wrapper.text()).toContain('Loading campaigns...');
  });

  /**
   * Test: Displaying Data
   * Description: Ensures the component renders a list of campaigns from the store.
   */
  it('should display a list of campaigns when data is available', async () => {
    mockStoreState = {
      campaigns: [
        { id: 1, name: 'Summer Sale', status: true, start_date: '2024-07-01', end_date: '2024-07-31', budget: 5000 },
      ],
    };
    const wrapper = mount(CampaignListView, { global: { stubs: { 'router-link': true, 'IconButton': true, 'PencilSquareIcon': true } } });
    await nextTick();
    expect(wrapper.text()).toContain('Summer Sale');
  });

});
