<script>
  import axios from 'axios';

  export default {
    name: 'Logout',
    mounted() {
      // Api Url
      const apiUrl = import.meta.env.VITE_API_URL;

      // Check if user is logged in
      const token = localStorage.getItem('token');
      if(!token) {
        this.$router.push({name: 'Login', params: { message: 'missingtoken'} });
      }
      axios.get(apiUrl + "/auth/verifytoken", {headers: {Authorization: `Token ${token}`}})
      .catch((error) => {this.$router.push({name: 'Login', params: { message: 'invalidtoken'} });});

      this.logout()
    },
    methods: {
      logout() {
        localStorage.removeItem('token');
        this.$router.push({name: 'Login', params: { message: 'logout'} });
      }
    }
  }
</script>

<template>
  <div class="d-inline-flex m-3" v-if="loading">
    <div class="spinner-border text-light"></div>
    <p class="px-2">Logging out...</p>
  </div>
</template>