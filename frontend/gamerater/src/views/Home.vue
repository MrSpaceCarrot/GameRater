<script setup>
  // Libraries & Components
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import apiClient from '@/axios';
  import NavBar from '../components/NavBar.vue';
  import GameTile from '../components/GameTile.vue';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faPlus, faDice, faDownload, faStar, faSkull, faFire} from '@fortawesome/free-solid-svg-icons';
  library.add(faDice, faPlus, faDownload, faStar, faSkull, faFire);

  // Variables
  const authStore = useAuthStore();
  const token = ref(authStore.token);
  let recentlyAddedGames = ref(null);
  let recentlyUpdatedGames = ref(null);
  let deadGames = ref(null);
  let randomGames = ref(null);
  let topGames = ref(null);

  // Functions
  // Fetch data from api
  function fetchFromAPI(url) {
    return apiClient
    .get(url, {headers: { Authorization: `Token ${token.value}` },})
    .then((response) => response.data)
    .catch((error) => {console.error("Error fetching data:", error); throw error;});
  }

  // Mounted
  onMounted(() => {
    // Get recently added games
    fetchFromAPI("/games/recentadd").then((data) => {recentlyAddedGames.value = data;})

    // Get recently updated games
    fetchFromAPI("/games/recentupdate").then((data) => {recentlyUpdatedGames.value = data})

    // Get dead games
    fetchFromAPI("games/dead").then((data) => {deadGames.value = data})

    // Get random games
    fetchFromAPI("/games/random").then((data) => {randomGames.value = data})

    // Get top games
    fetchFromAPI("/games/top").then((data) => {topGames.value = data})
  });
</script>

<template>
  <NavBar />
  <div class="container-fluid">
    <h2 class="text-light py-2">Home</h2>

    <!-- Random games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-dice" /> Random Games</h5>
    <div v-if="randomGames" class="row justify-content-start gx-2">
      <div v-for="game in randomGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2">
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
                    :popularity-score="game.popularity_score"
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Random games -->

    <!-- Recently added games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-plus" /> Recently Added Games</h5>
    <div v-if="recentlyAddedGames" class="row justify-content-start">
      <div v-for="game in recentlyAddedGames" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 gx-2">
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
                  :popularity-score="game.popularity_score"
          />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently added games -->

    <!-- Recently updated games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-download" /> Recently Updated Games</h5>
    <div v-if="recentlyUpdatedGames" class="row justify-content-start">
      <div v-for="game in recentlyUpdatedGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 gx-2">
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
                    :popularity-score="game.popularity_score"
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently updated games -->

    <!-- Top games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-fire" /> Most Popular Games</h5>
    <div v-if="topGames" class="row justify-content-start">
      <div v-for="game in topGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 gx-2">
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
                    :popularity-score="game.popularity_score"
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Top games -->

    <!-- Recently updated games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-skull" /> Dead Games</h5>
    <div v-if="deadGames" class="row justify-content-start">
      <div v-for="game in deadGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 gx-2">
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
                    :popularity-score="game.popularity_score"
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently updated games -->
  </div>
</template>