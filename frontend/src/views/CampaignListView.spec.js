import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import IconButton from '../components/IconButton.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import { nextTick } from 'vue';

beforeEach(() => {
  // Ensure module cache is cleared between tests so we can re-mock the store
  vi.resetModules();
});

describe('CampaignListView', () => {
  it('shows empty state when there are no campaigns', async () => {
    // Mock the campaign store to return no campaigns
    vi.mock('../stores/campaignStore', () => {
      const { ref } = require('vue');
      const { vi } = require('vitest');
      return {
        useCampaignStore: () => ({
          campaigns: ref([]),
          isLoading: ref(false),
          fetchCampaigns: vi.fn(),
          deleteCampaign: vi.fn(),
          toggleCampaign: vi.fn(),
          error: null,
        }),
      };
    });

    const { default: CampaignListView } = await import('./CampaignListView.vue');

    const wrapper = mount(CampaignListView, {
      global: {
        stubs: { 'router-link': true },
        components: { IconButton, ConfirmModal },
      },
    });

    expect(wrapper.text()).toContain('No campaigns found');
  });

  it('calls toggleCampaign and deleteCampaign when action buttons are clicked and confirmed', async () => {
    const deleteMock = vi.fn();
    const toggleMock = vi.fn();

    // Mock the campaign store with one campaign
    vi.mock('../stores/campaignStore', () => {
      const { ref } = require('vue');
      return {
        useCampaignStore: () => ({
          campaigns: ref([
            {
              id: 1,
              name: 'Test Campaign',
              description: 'A short test',
              status: true,
              start_date: '2024-01-01',
              end_date: '2024-01-10',
              budget: 1234,
            },
          ]),
          isLoading: ref(false),
          fetchCampaigns: vi.fn(),
          deleteCampaign: deleteMock,
          toggleCampaign: toggleMock,
          error: null,
        }),
      };
    });

    const { default: CampaignListView } = await import('./CampaignListView.vue');

    const wrapper = mount(CampaignListView, {
      global: {
        stubs: { 'router-link': true },
        components: { IconButton, ConfirmModal },
      },
    });

    // Find and click the toggle button (title set to 'Deactivate' for status=true)
    const toggleBtn = wrapper.find('button[title="Deactivate"]');
    expect(toggleBtn.exists()).toBe(true);
    await toggleBtn.trigger('click');

    // Wait for modal to render
    await nextTick();
    const confirmOk = wrapper.find('[data-test="confirm-ok"]');
    expect(confirmOk.exists()).toBe(true);
    await confirmOk.trigger('click');

    expect(toggleMock).toHaveBeenCalledWith(1);

    // Find and click the delete button
    const deleteBtn = wrapper.find('button[title="Delete"]');
    expect(deleteBtn.exists()).toBe(true);
    await deleteBtn.trigger('click');

    // Wait for modal and confirm
    await nextTick();
    const confirmOk2 = wrapper.find('[data-test="confirm-ok"]');
    expect(confirmOk2.exists()).toBe(true);
    await confirmOk2.trigger('click');

    expect(deleteMock).toHaveBeenCalledWith(1);
  });
});
