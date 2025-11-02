// Debugging test file: Contains only the single failing test.

import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import CampaignListView from '../src/views/CampaignListView.vue';

// A completely static, non-reactive mock. The simplest possible scenario.
vi.mock('../src/stores/campaignStore', () => ({
  useCampaignStore: () => ({
    campaigns: [],
    isLoading: false, // Hardcoded to false
    error: null,
    fetchCampaigns: vi.fn(),
  }),
}));

describe('CampaignListView.vue - ISOLATION TEST', () => {

  it('should show the empty state and NOT the loading state', () => {
    // Act: Mount the component with the simplest possible mock.
    const wrapper = mount(CampaignListView, {
      global: { stubs: { 'router-link': true } },
    });

    // Assert: Check the initial, synchronous render state.
    const html = wrapper.html();
    console.log("COMPONENT HTML:", html);

    expect(html).toContain('No campaigns found');
    expect(html).not.toContain('Loading campaigns...');
  });

});
