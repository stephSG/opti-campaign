import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { nextTick } from 'vue';
import CampaignListView from '../src/views/CampaignListView.vue';

// --- Mocking Strategy ---
// Instead of using reactive refs, which caused state leakage between tests,
// we now use a simple variable `mockStoreState`. 
// Before each test, we can set this variable to whatever state we need.
let mockStoreState = {};

vi.mock('../src/stores/campaignStore', () => ({
  // The store will now return a fresh object based on the current `mockStoreState`.
  useCampaignStore: () => ({
    campaigns: [],
    isLoading: false,
    error: null,
    // Spread the current test's state
    ...mockStoreState,
    // Mock functions to prevent them from running their actual code
    fetchCampaigns: vi.fn(),
    deleteCampaign: vi.fn(),
    toggleCampaign: vi.fn(),
  }),
}));

describe('CampaignListView.vue', () => {

  // Before each test, clear all mocks to ensure a clean slate.
  beforeEach(() => {
    vi.clearAllMocks();
  });

  /**
   * Test: Loading State
   * Description: This test verifies that the component correctly displays the 
   * loading indicator when the store's `isLoading` state is true.
   */
  it('should show a loading message when isLoading is true', async () => {
    // Arrange: Set the mock store state for this specific test.
    mockStoreState = {
      isLoading: true,
    };

    // Act: Mount the component. It will use the state defined above.
    const wrapper = mount(CampaignListView, {
      global: { stubs: { 'router-link': true } },
    });
    await nextTick(); // Wait for Vue to render the state change.

    // Assert: The loading message should be visible.
    expect(wrapper.text()).toContain('Loading campaigns...');
  });

  /**
   * Test: Displaying Data
   * Description: This test ensures that when the store provides a list of campaigns,
   * the component renders them correctly in the view.
   */
  it('should display a list of campaigns when data is available', async () => {
    // Arrange: Set the mock store state with campaign data.
    mockStoreState = {
      isLoading: false,
      campaigns: [
        { id: 1, name: 'Summer Sale', description: 'Big discounts', status: true, start_date: '2024-07-01', end_date: '2024-07-31', budget: 5000 },
        { id: 2, name: 'Winter Promo', description: 'Cold deals', status: false, start_date: '2024-12-01', end_date: '2024-12-31', budget: 3000 },
      ],
    };

    // Act: Mount the component.
    const wrapper = mount(CampaignListView, {
      global: { stubs: { 'router-link': true, 'IconButton': true, 'PencilSquareIcon': true } },
    });
    await nextTick();

    // Assert: Check that campaign names are visible and the empty message is not.
    const componentText = wrapper.text();
    expect(componentText).toContain('Summer Sale');
    expect(componentText).toContain('Winter Promo');
    expect(componentText).not.toContain('No campaigns found');

    // Assert: Check that the correct number of table rows are rendered.
    const tableRows = wrapper.findAll('tbody tr');
    expect(tableRows.length).toBe(2);
  });

});
