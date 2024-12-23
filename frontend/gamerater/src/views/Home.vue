<script setup>
  // Libraries & Components
  import { inject, ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import axios from 'axios';
  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faPencil } from '@fortawesome/free-solid-svg-icons';
  import { faGamepad } from '@fortawesome/free-solid-svg-icons';
  library.add(faSteam, faPencil, faGamepad);
  import NavBar from '../components/NavBar.vue';
  import GameTile from '../components/GameTile.vue';

  // Variables
  const config = inject('config');
  const authStore = useAuthStore();
  const token = ref(authStore.token);
  const apiUrl = ref(config.API_URL);
  let recentlyAddedGames = ref(null);
  let recentlyUpdatedGames = ref(null);
  let deadGames = ref(null);
  let randomGames = ref(null);

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
    fetchFromAPI(`${apiUrl.value}/games/recentadd`).then((data) => {recentlyAddedGames.value = data;})

    // Get recently updated games
    fetchFromAPI(`${apiUrl.value}/games/recentupdate`).then((data) => {recentlyUpdatedGames.value = data})

    // Get dead games
    fetchFromAPI(`${apiUrl.value}/games/dead`).then((data) => {deadGames.value = data})

    // Get random games
    fetchFromAPI(`${apiUrl.value}/games/random`).then((data) => {randomGames.value = data})
  });
</script>

<template>
  <NavBar />
  <div class="container-fluid">
    <h2 class="text-light py-2">Home</h2>

    <!-- Random games -->
    <h5 class="text-light">Random Games</h5>
    <div v-if="randomGames" class="row justify-content-start pb-2">
      <div v-for="game in randomGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 py-2">
         <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_link" 
                    :date="game.last_updated"
                    date-text="Updated"
                    :tags="game.tags"
                    :min-party-size="game.min_party_size" 
                    :max-party-size="game.max_party_size" 
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Random games -->

    <!-- Recently added games -->
    <h5 class="text-light">Recently Added Games</h5>
    <div v-if="recentlyAddedGames" class="row justify-content-start pb-2">
      <div v-for="game in recentlyAddedGames" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 py-2">
        <GameTile :name="game.name" 
                  :platform="game.platform"
                  :install-size="game.install_size"
                  :link="game.link" 
                  :banner-link="game.banner_link" 
                  :date="game.date_added"
                  date-text="Added"
                  :tags="game.tags"
                  :min-party-size="game.min_party_size" 
                  :max-party-size="game.max_party_size"
          />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently added games -->

    <!-- Recently updated games -->
    <h5 class="text-light">Recently Updated Games</h5>
    <div v-if="recentlyUpdatedGames" class="row justify-content-start pb-2">
      <div v-for="game in recentlyUpdatedGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 py-2">
          <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_link" 
                    :date="game.last_updated"
                    date-text="Updated"
                    :tags="game.tags"
                    :min-party-size="game.min_party_size" 
                    :max-party-size="game.max_party_size" 
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently updated games -->

    <!-- Recently updated games -->
    <h5 class="text-light">Dead Games</h5>
    <div v-if="deadGames" class="row justify-content-start pb-2">
      <div v-for="game in deadGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 py-2">
         <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_link" 
                    :date="game.last_updated"
                    date-text="Updated"
                    :tags="game.tags"
                    :min-party-size="game.min_party_size" 
                    :max-party-size="game.max_party_size" 
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently updated games -->
  </div>
</template>