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
  <div>
    <p v-if="loading">Logging out...</p>
  </div>
</template>