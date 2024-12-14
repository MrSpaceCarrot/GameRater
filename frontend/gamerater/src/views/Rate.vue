<script setup>
  // Libraries & Components
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import axios from 'axios';
  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faPencil } from '@fortawesome/free-solid-svg-icons';
  import { faGamepad } from '@fortawesome/free-solid-svg-icons';
  library.add(faSteam, faPencil, faGamepad);
  import NavBar from '../components/NavBar.vue';

  // Variables
  const authStore = useAuthStore();
  const token = ref(authStore.token);
  const apiUrl = ref(import.meta.env.VITE_API_URL);
  let allGames = ref(null);

  // Functions
  // Fetch data from api
  function fetchFromAPI(url) {
    return axios
    .get(url, {headers: { Authorization: `Token ${token.value}` },})
    .then((response) => response.data)
    .catch((error) => {console.error("Error fetching data:", error); throw error;});
  }

  // Set alternating backgrounc colors
  function getBackground(index) {
    return index % 2 === 0 ? 'bglight' : 'bgdark';
  }

  // Mounted
  onMounted(() => {
    // Get all games
    fetchFromAPI(`${apiUrl.value}/games/`).then((data) => {allGames.value = data;})
  });
</script>

<template>
  <NavBar />
  <div class="container px-5">
    <h2 class="text-light py-2">Your Ratings</h2>

    <div v-if="allGames" class="row">
      <div v-for="(game, index) in allGames" :key="game.id" class="text-center py-1" :class="getBackground(index)">
          <div class="row align-middle">
            <div class="col-sm-2 text-start "><span class="my-0">{{ game.name }}</span></div>
            <div class="col btn-group">
              <button type="button" class="btn btn-sm btn-danger">Terrible 🤮</button>
              <button type="button" class="btn btn-sm btn-danger">Bad 👎</button>
              <button type="button" class="btn btn-sm btn-danger">Eh 🙁</button>
              <button type="button" class="btn btn-sm btn-secondary">Neutral 😐</button>
              <button type="button" class="btn btn-sm btn-success">Ok 🙂</button>
              <button type="button" class="btn btn-sm btn-success">Good 👍</button>
              <button type="button" class="btn btn-sm btn-success">Peak 🔥</button>
            </div>
            <div class="col">
              <img :src="game.banner_link" :alt="`${game.name} banner image`" class="img-fluid rateimage">
            </div>
          </div>
      </div>
    </div>
    <p v-else>Loading...</p>
</div>

</template>

<style scoped>

.bglight {
  background-color: #373d48;
}

.bgdark {
  background-color: #2c313c;
}

span {
  color: #fff;
}

.rateimage {
  max-height: 50px;
}

</style>