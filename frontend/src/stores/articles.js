import { defineStore } from 'pinia';

export const useArticleStore = defineStore('articles', {
  state: () => ({
    articles: [],
  }),
  actions: {
    async fetchArticles() {
      try {
        const response = await fetch('/api/articles'); // Adjust API endpoint as necessary
        if (!response.ok) {
          throw new Error('Failed to fetch articles');
        }
        this.articles = await response.json();
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    },
  },
});