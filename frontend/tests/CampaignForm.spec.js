import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import CampaignForm from '../src/components/CampaignForm.vue';

describe('CampaignForm.vue', () => {
  const mountOptions = {
    global: {
      // Stub child components to prevent render errors and keep tests focused.
      stubs: {
        'router-link': true,
        'XMarkIcon': true,
        'CheckIcon': true,
      },
    },
  };

  /**
   * Test: Component Mounting
   * Description: Verifies that the component renders without crashing.
   */
  it('should mount a component', () => {
    const wrapper = mount(CampaignForm, mountOptions);
    expect(wrapper.exists()).toBe(true);
  });

  /**
   * Test: Form Submission
   * Description: This test verifies that when a user fills out the form
   * and submits it, the component emits a 'submitForm' event with the
   * correct data payload.
   */
  it('should emit submitForm with the form data when submitted', async () => {
    // Arrange: Mount the component.
    const wrapper = mount(CampaignForm, mountOptions);
    const randomCampaignName = `Test Campaign ${Date.now()}`;

    // Act: Find the name input, set its value, and then submit the form.
    await wrapper.find('input#name').setValue(randomCampaignName);
    await wrapper.find('form').trigger('submit');

    // Assert 1: Check that the 'submitForm' event was emitted.
    expect(wrapper.emitted()).toHaveProperty('submitForm');

    // Assert 2: Check that the emitted event has the correct payload.
    // wrapper.emitted('submitForm') returns an array of emissions. We check the first one.
    const submittedPayload = wrapper.emitted('submitForm')[0][0];
    expect(submittedPayload.name).toBe(randomCampaignName);
  });
});
