// Summary:
// This file contains unit tests for the CampaignForm.vue component.
// The tests check if the component renders correctly and if the
// input field for the campaign name exists.

import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import CampaignForm from '../src/components/CampaignForm.vue';

describe('CampaignForm.vue', () => {
  const mountOptions = {
    global: {
      stubs: {
        'router-link': true, // Stub <router-link>
      },
    },
  };

  // Test case to check if the component mounts correctly.
  it('should mount a component', () => {
    const wrapper = mount(CampaignForm, mountOptions);
    // Expect the component to exist.
    expect(wrapper.exists()).toBe(true);
  });

  // Test case to check if the campaign name input field exists.
  it('should have a campaign name input field', async () => {
    const wrapper = mount(CampaignForm, mountOptions);
    // Find an input with the id "name".
    const nameInput = wrapper.find('input#name');
    expect(nameInput.exists()).toBe(true);
  });
});
