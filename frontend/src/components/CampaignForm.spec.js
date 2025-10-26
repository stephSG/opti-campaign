import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import CampaignForm from './CampaignForm.vue';

describe('CampaignForm.vue', () => {
  const mountOptions = {
    global: {
      stubs: {
        'router-link': true, // Remplace <router-link> par un substitut
      },
    },
  };

  it('devrait se monter correctement', () => {
    const wrapper = mount(CampaignForm, mountOptions);
    // Vérifie que le composant est bien monté
    expect(wrapper.exists()).toBe(true);
  });

  it('devrait contenir un champ de saisie pour le nom de la campagne', async () => {
    const wrapper = mount(CampaignForm, mountOptions);
    // Recherche un input avec l'id "name"
    const nameInput = wrapper.find('input#name');
    expect(nameInput.exists()).toBe(true);
  });
});
