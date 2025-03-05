<script setup>
  // Libraries & Components
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import apiClient from '@/axios';
  import NavBar from '../components/NavBar.vue';
  import GameTile from '../components/GameTile.vue';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faPlus, faDice, faDownload, faStar, faSkull, faFire, faChevronLeft, faChevronRight} from '@fortawesome/free-solid-svg-icons';
  library.add(faDice, faPlus, faDownload, faStar, faSkull, faFire, faChevronLeft, faChevronRight);

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

  // Scroll
  function scroll(category, scrollType) {
    const categoryElement = document.getElementById(category)
    const childWidth = categoryElement.firstElementChild.offsetWidth;

    if (scrollType === 'reset') {
      categoryElement.scrollX = 0;
      
    } else if (scrollType === 'right') {
      categoryElement.scrollBy({ left: 1 * childWidth, behavior: 'smooth' });
    } else {
      categoryElement.scrollBy({ left: -1 * childWidth, behavior: 'smooth' });
    }
  }

  // Mounted
  onMounted(() => {
    // Get games lists
    fetchFromAPI("/games/recentadd").then((data) => {recentlyAddedGames.value = data})
    fetchFromAPI("/games/recentupdate").then((data) => {recentlyUpdatedGames.value = data})
    fetchFromAPI("games/dead").then((data) => {deadGames.value = data})
    fetchFromAPI("/games/random").then((data) => {randomGames.value = data})
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
        <button @click="scroll('randomGames', 'left')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-left" />
        </button>
      </div>

      <div v-if="randomGames" id="randomGames" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 justify-content-start gx-2 scrollbox" @load="scroll('randomGames', 'reset')">
        <div v-for="game in randomGames" :key="game.id" class="col text-center">
          <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_image_url" 
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

      <div style="max-width: 50px;">
        <button @click="scroll('randomGames', 'right')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />
        </button>
      </div>
    </div>
    <!-- /Random games -->

    <!-- Recently added games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-plus" /> Recently Added Games</h5>
    <div class="categorydisplay w-100 mb-3">
      <div style="max-width: 50px;">
        <button @click="scroll('recentlyAddedGames', 'left')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-left" />
        </button>
      </div>

      <div v-if="recentlyAddedGames" id="recentlyAddedGames" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 justify-content-start gx-2 scrollbox">
        <div v-for="game in recentlyAddedGames" :key="game.id" class="col text-center">
          <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_image_url" 
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

      <div style="max-width: 50px;">
        <button @click="scroll('recentlyAddedGames', 'right')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />
        </button>
      </div>
    </div>
    <!-- /Recently added games -->

    <!-- Recently updated games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-download" /> Recently Updated Games</h5>
    <div class="categorydisplay w-100 mb-3">
      <div style="max-width: 50px;">
        <button @click="scroll('recentlyUpdatedGames', 'left')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-left" />
        </button>
      </div>

      <div v-if="recentlyUpdatedGames" id="recentlyUpdatedGames" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 justify-content-start gx-2 scrollbox">
        <div v-for="game in recentlyUpdatedGames" :key="game.id" class="col text-center">
          <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_image_url" 
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

      <div style="max-width: 50px;">
        <button @click="scroll('recentlyUpdatedGames', 'right')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />
        </button>
      </div>
    </div>
    <!-- /Recently updated games -->

    <!-- Top games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-fire" /> Most Popular Games</h5>
    <div class="categorydisplay w-100 mb-3">
      <div style="max-width: 50px;">
        <button @click="scroll('topGames', 'left')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-left" />
        </button>
      </div>

      <div v-if="topGames" id="topGames" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 justify-content-start gx-2 scrollbox">
        <div v-for="game in topGames" :key="game.id" class="col text-center">
          <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_image_url" 
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

      <div style="max-width: 50px;">
        <button @click="scroll('topGames', 'right')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />
        </button>
      </div>
    </div>
    <!-- /Top games -->




    <!-- Dead games -->
    <h5 class="text-light pb-1"><font-awesome-icon icon="fa-solid fa-skull" /> Dead Games</h5>
    <div class="categorydisplay w-100 mb-3">
      <div style="max-width: 50px;">
        <button @click="scroll('deadGames', 'left')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-left" />
        </button>
      </div>

      <div v-if="deadGames" id="deadGames" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 justify-content-start gx-2 scrollbox">
        <div v-for="game in deadGames" :key="game.id" class="col text-center">
          <GameTile :name="game.name" 
                    :platform="game.platform"
                    :install-size="game.install_size"
                    :link="game.link" 
                    :banner-link="game.banner_image_url" 
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

      <div style="max-width: 50px;">
        <button @click="scroll('deadGames', 'right')" type="button" class="btn bg-dark text-light w-100 h-100 px-0 mx-0">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />
        </button>
      </div>
    </div>
    <!-- /Dead games -->
  </div>
</template>

<style >

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