// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import NewsPage from '../components/NewsPage.vue';
import ProfilePage from '../components/ProfilePage.vue'; // Import the new component

const routes = [
  { path: '/profile', name: 'profile', component: ProfilePage }, // Add the profile route
  { path: '/news', component: NewsPage },
  // Add other routes as needed
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

