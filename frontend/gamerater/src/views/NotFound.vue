<script>
  import axios from 'axios';

  import NavBar from '../components/NavBar.vue'

  export default {
    name: 'NotFound',
    components: {
      NavBar
    },
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
    }
  }
</script>

<template>
    <NavBar />
    <div class="container-fluid">
    <h2 class="text-light py-2">404 Page Not Found</h2>
  </div>
</template>