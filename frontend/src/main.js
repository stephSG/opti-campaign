import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

// Import the global Tailwind CSS file
import './index.css';

// 1. Initialize the Vue App
const app = createApp(App);

// 2. Initialize Pinia (state management)
const pinia = createPinia();

// 3. Use Pinia
app.use(pinia);

// 4. Use Vue Router
app.use(router);

// 5. Mount the app to the DOM
app.mount('#app');
