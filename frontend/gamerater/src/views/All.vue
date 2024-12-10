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

  // Mounted
  onMounted(() => {
    // Get recently added games
    fetchFromAPI(`${apiUrl.value}/games/`).then((data) => {allGames.value = data;})
  });
</script>

<template>
  <NavBar />
  <div class="container-fluid">
    <h2 class="text-light py-2">All Games</h2>

    <div v-if="allGames" class="row justify-content-start">
      <div v-for="game in allGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 py-2">
          <div class="imgcontainer rounded">
            <a :href="game.link" target="_blank">
                <img :src="game.banner_link" :alt="`${game.name} banner image`" class="img-fluid hoverfade fixedsize">
            </a>
          </div>
          <div class="gametitle">
            <p class="text-light pt-1">{{ game.name }} 
            <img v-if="game.platform === 'Roblox'" src="/roblox.svg" alt="Roblox Logo" class="inline-svg">
            <font-awesome-icon v-else-if="game.platform ==='Steam'" icon="fa-brands fa-steam" />
            <font-awesome-icon v-else-if="game.platform ==='Party'" icon="fa-solid fa-pencil" />
            <font-awesome-icon v-else-if="game.platform ==='Other'" icon="fa-solid fa-gamepad" />
            </p>
        </div>
      </div>
    </div>
    <p v-else>Loading...</p>
</div>

</template>

<style>

.imgcontainer {
    position: relative;
    width: 100%;
    padding-top: 56.25%;
    overflow: hidden; 
    border-radius: inherit;
}

.fixedsize {
    position: absolute;
    top: 0;
    left: 50%;
    min-height: 100%;
    width: auto;
    transform: translateX(-50%);
    object-fit: cover;
}

.hoverfade {
    transition: all 0.2s ease-in-out 0s;
}

.hoverfade:hover {
    opacity: 0.5;
}

.gametitle {
    text-align: center;
}

.inline-svg {
    width: 1.1em;
    height: 1.1em;
    vertical-align: middle;
    margin-top: -3px;
}

</style>