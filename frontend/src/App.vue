<!-- src/App.vue -->
<template>
  <div>
    <nav>
      <router-link to="/profile">Profile</router-link>
      <router-link to="/news">News</router-link>
    </nav>

    <router-view />
  </div>
</template>

<script>

export default {
  data() {
    return {
      authenticated: false,
      userProfile: {},
    };
  },
  watch: {
    $route(to, from) {
      if (to.name === 'profile') {
        this.authenticated = true;
      } else {
        this.authenticated = false;
      }
    },
  },
};
</script>
