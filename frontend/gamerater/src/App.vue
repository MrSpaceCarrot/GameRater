<script>
  import navbar from './components/navbar.vue';
  import all from './components/all.vue';

  export default {
    name: 'App',
    components: {
      navbar,
      all,
    },

    data() {
      return {
        
      };
    }
  }
</script>

<template>
  <navbar />
  <all />
</template>

<style>

body {
  margin: 0px;
  padding: 0px;
  background-color: #2c313c;
}

p, li {
  color: #fff;
}

</style>