<script>
  import NavBar from '../components/NavBar.vue'

  export default {
    name: 'Home',
    components: {
      NavBar
    }
  }
</script>

<template>
  <NavBar />
  <div class="container-fluid">
    <h2 class="text-light py-2">Home Page</h2>
  </div>
</template>