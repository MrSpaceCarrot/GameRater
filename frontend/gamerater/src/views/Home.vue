<script setup>
  // Libraries & Components
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import apiClient from '@/axios';
  import NavBar from '../components/NavBar.vue';
  import GameTile from '../components/GameTile.vue';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faPlus, faDice, faDownload, faStar, faSkull, faChevronLeft, faChevronRight} from '@fortawesome/free-solid-svg-icons';
  library.add(faDice, faPlus, faDownload, faStar, faSkull, faChevronLeft, faChevronRight);

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

  function scroll(category, scrollRight) {
    const categoryElement = document.getElementById(category)
    const childWidth = categoryElement.firstElementChild.offsetWidth;
    if (scrollRight === true) {
      categoryElement.scrollBy({ left: 1 * childWidth, behavior: 'smooth' });
    } else {
      categoryElement.scrollBy({ left: -1 * childWidth, behavior: 'smooth' });
    }
    
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
    <div class="categorydisplay w-100 mb-3">

      <div style="max-width: 50px;">
        <button @click="scroll('randomGames', false)" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-left" />
        </button>
      </div>

      <div class="">

        <div v-if="randomGames" id="randomGames" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 justify-content-start gx-2 scrollbox">
          <div v-for="game in randomGames" :key="game.id" class="col text-center">
            <img :src="game.banner_link" :alt="`${game.name} banner image`" class="img-fluid hoverfade fixedsize">  
          </div>  
        </div>

        <!--

        <GameTile class="h-100"
                          name="Arsenal" 
                          platform="Roblox"
                          link="https://www.roblox.com/games/286090429/Arsenal" 
                          banner-link="https://tr.rbxcdn.com/180DAY-a8abe703dec5b81538e04a714ab7dca4/768/432/Image/Webp/noFilter" 
                          date="2025-01-03T18:17:50+13:00"
                          date-text="Updated"
                          tags="1"
                          min-party-size="1"
                          max-party-size="16" 
                  />

        -->

        <!--

        <div class="container-fluid">
          <div v-if="randomGames" id="randomGames" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 justify-content-start gx-2 scrollbox">
            <div v-for="game in randomGames" :key="game.id" class="col">
              <GameTile class="h-100"
                          :name="game.name" 
                          :platform="game.platform"
                          :install-size="game.install_size"
                          :link="game.link" 
                          :banner-link="game.banner_link" 
                          :date="game.last_updated"
                          date-text="Updated"
                          :tags="game.tags"
                          :min-party-size="game.min_party_size" 
                          :max-party-size="game.max_party_size" 
                          :average-rating="game.average_rating"
                  />
            </div>
          </div>
          <p v-else>Loading...</p>
        </div>

        -->
      </div>

      <div style="max-width: 50px;">
        <button @click="scroll('randomGames', true)" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />
        </button>
      </div>

    </div>
    <!-- /Random games -->

    <!-- Recently added games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-plus" /> Recently Added Games</h5>
    <div v-if="recentlyAddedGames" id="recentlyAddedGames" class="row justify-content-start">
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
                  :average-rating="game.average_rating"
          />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently added games -->

    <!-- Recently updated games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-download" /> Recently Updated Games</h5>
    <div v-if="recentlyUpdatedGames" id="recentlyAddedGames" class="row justify-content-start">
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
                    :average-rating="game.average_rating"
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently updated games -->

    <!-- Top games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-star" /> Top User Rated Games</h5>
    <div v-if="topGames" id="topGames" class="row justify-content-start">
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
                    :average-rating="game.average_rating"
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Top games -->

    <!-- Recently updated games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-skull" /> Dead Games</h5>
    <div v-if="deadGames" id="deadGames" class="row justify-content-start">
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
                    :average-rating="game.average_rating"
            />
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently updated games -->
  </div>
</template>

<style>

.scrollbox {
  display: flex;
  max-width: 100vw;
  overflow-x: scroll;
  flex-direction: row;
  flex-wrap: nowrap;
  scrollbar-width: none;
}

.categorydisplay {
  display: grid;
  grid-template-columns: 20px 1fr 20px;
  gap: 10px;
}

</style>