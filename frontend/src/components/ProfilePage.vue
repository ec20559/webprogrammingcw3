<template>
  
  <div v-if="user" class="user-profile">
    <h1>{{ user.username }}</h1>

    <div class="profile-picture">
      <label>Profile Picture:</label>
      <img :src="user.profile_image" alt="Profile Image" v-if="user.profile_image" />
    </div>

    <div>
      <p v-if="user.email">Email: {{ user.email }}</p>
      <p v-if="user.date_of_birth">Date of Birth: {{ user.date_of_birth }}</p>

      <!-- Add the input field for updating email -->
      <div>
        <label for="email">Email:</label>
        <input v-model="editedUser.email" type="email" placeholder="Enter new email">
        <!-- Add the "Save" button for email -->
        <button @click="saveEmail">Save Email</button>
      </div>

      <!-- Add the input field for updating date of birth -->
      <div>
        <label for="dateOfBirth">Date of Birth:</label>
        <input v-model="editedUser.date_of_birth" type="date">
        <!-- Add the "Save" button for date of birth -->
        <button @click="saveDateOfBirth">Save Date of Birth</button>
      </div>

      <!-- Add the input field for updating profile picture -->
      <div>
        <label for="profilePicture">Profile Picture URL:</label>
        <input v-model="editedUser.profile_image" type="text" placeholder="Enter new profile picture URL">
        <!-- Add the "Save" button for profile picture -->
        <button @click="saveProfilePicture">Save Profile Picture</button>
      </div>

      <!-- Display the favorite topic dropdown -->
      <div>
        <label for="favoriteTopic">Favorite Topic:</label>
        <select v-model="user.favorite_topic" @change="fetchArticlesByCategory">
          <option value="None">None</option>
          <option value="Sports">Sports</option>
          <option value="World News">World News</option>
        </select>

        <!-- Add the "Save" button for favorite topic -->
        <button @click="saveFavoriteTopic">Save Topic</button>
      </div>

      <!-- Display articles based on the selected category -->
      <div v-if="selectedCategory">
        <h2>{{ selectedCategory.category }}</h2>
        <ul>
          <li v-for="article in selectedCategory.articles" :key="article.id">
            <h3>{{ article.title }}</h3>
            <p>{{ article.contents }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>
    <p>Loading user profile...</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      editedUser: {
        email: '',
        date_of_birth: '',
        profile_image: '',
      },
      selectedCategory: null,
    };
  },
  async mounted() {
    await this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await fetch('http://localhost:8000/api/get_user_profile/', {
          credentials: 'include',
        });

        const data = await response.json();
        this.user = data;

        // Fetch articles based on the initial favorite topic
        this.fetchArticlesByCategory();
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    },
    async fetchArticlesByCategory() {
      try {
        const response = await fetch('http://localhost:8000/api/get_articles/', {
          credentials: 'include',
        });

        const data = await response.json();
        this.articles = this.groupArticlesByCategory(data);

        // Filter articles based on the selected category
        this.selectedCategory = this.articles.find(
          (category) => category.category === this.user.favorite_topic
        );
      } catch (error) {
        console.error('Error fetching news articles:', error);
      }
    },
    async saveEmail() {
      try {
        // Get CSRF token from cookies
        const csrfToken = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          .split('=')[1];

        console.log('CSRF Token:', csrfToken);

        // Your existing code to make the API request
        const response = await fetch('http://localhost:8000/api/update_user_email/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
          body: JSON.stringify({ email: this.editedUser.email }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Email updated:', data);

          // Optionally, fetch the user profile again to update the displayed data
          await this.fetchUserProfile();
        } else {
          console.error('Error updating email:', response.statusText);
        }
      } catch (error) {
        console.error('Network error:', error);
      }
    },
    async saveDateOfBirth() {
      try {
        // Get CSRF token from cookies
        const csrfToken = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          .split('=')[1];

        console.log('CSRF Token:', csrfToken);

        const response = await fetch('http://localhost:8000/api/update_user_date_of_birth/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
          body: JSON.stringify({ date_of_birth: this.editedUser.date_of_birth }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Date of Birth updated:', data);

          await this.fetchUserProfile();
        } else {
          console.error('Error updating date of birth:', response.statusText);
        }
      } catch (error) {
        console.error('Network error:', error);
      }
    },
    async saveProfilePicture() {
      try {
        // Get CSRF token from cookies
        const csrfToken = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          .split('=')[1];

        console.log('CSRF Token:', csrfToken);

        const response = await fetch('http://localhost:8000/api/update_user_profile_picture/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
          body: JSON.stringify({ profile_image: this.editedUser.profile_image }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Profile Picture updated:', data);

          // Optionally, fetch the user profile again to update the displayed data
          await this.fetchUserProfile();
        } else {
          console.error('Error updating profile picture:', response.statusText);
        }
      } catch (error) {
        console.error('Network error:', error);
      }
    },
    async saveFavoriteTopic() {
      try {
        const response = await fetch('http://localhost:8000/api/update_favorite_topic/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({ favorite_topic: this.user.favorite_topic }),
        });

        const data = await response.json();
        console.log('Favorite topic updated:', data);

        // Optionally, fetch the user profile again to update the displayed data
        await this.fetchUserProfile();
      } catch (error) {
        console.error('Error updating favorite topic:', error);
      }
    },
    groupArticlesByCategory(articles) {
      // Group articles by category
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
  },
};
</script>

<style scoped>
/* Add your component styles here */
.profile-picture {
  margin-top: 10px;
}

/* Add styles as needed */
</style>
