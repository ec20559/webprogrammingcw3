<template>
  <div>
    <h1>Welcome to the News Page</h1>
    <div v-if="articles">
      <div v-for="category in articles" :key="category.category">
        <h2>{{ category.category }}</h2>
        <ul>
          <li v-for="article in category.articles" :key="article.id">
            <h3>{{ article.title }}</h3>
            <p>{{ article.contents }}</p>
            <div v-if="article.comments.length > 0">
              <h4>Comments:</h4>
              <ul>
                <li v-for="comment in article.comments" :key="comment.id">
                  <p>{{ comment.text }}</p>
                </li>
              </ul>
            </div>
            <textarea v-model="newCommentText[article.id]"></textarea>
            <button @click="addComment(article)">Add Comment</button>
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      <p>Loading news articles...</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      articles: null,
      newCommentText: {}, // Object to store new comments for each article
    };
  },
  async mounted() {
    await this.fetchArticles();
  },
  methods: {
    async fetchArticles() {
      try {
        const response = await fetch('http://localhost:8000/api/get_articles/', {
          credentials: 'include',
        });

        const data = await response.json();
        this.articles = this.groupArticlesByCategory(data);
      } catch (error) {
        console.error('Error fetching news articles:', error);
      }
    },
    async addComment(article) {
      try {
        // Get CSRF token from cookies
        const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

        console.log('CSRF Token:', csrfToken);

        const response = await fetch('http://localhost:8000/api/update_article_comments/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
          body: JSON.stringify({
            articleId: article.id,
            text: this.newCommentText[article.id],
          }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Comment added:', data);

          // Update the comments locally without fetching all articles again
          const updatedArticle = this.findArticleById(article.id);
          if (updatedArticle) {
            updatedArticle.comments.push(data.comment);

            this.newCommentText[article.id] = '';
          }
        } else {
          console.error('Error adding comment:', response.statusText);
        }
      } catch (error) {
        console.error('Network error:', error);
      }
    },
    groupArticlesByCategory(articles) {
      const groupedArticles = articles.reduce((acc, article) => {
        const category = article.topic;
        if (!acc[category]) {
          acc[category] = { category, articles: [] };
        }
        acc[category].articles.push(article);
        return acc;
      }, {});
      return Object.values(groupedArticles);
    },
    findArticleById(articleId) {
      for (const category of this.articles) {
        const foundArticle = category.articles.find(article => article.id === articleId);
        if (foundArticle) {
          return foundArticle;
        }
      }
      return null;
    },
  },
};
</script>
