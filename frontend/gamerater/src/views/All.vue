<script setup>
  // Libraries & Components
  import { ref, onMounted, watch } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import apiClient from '@/axios';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faCircleXmark } from '@fortawesome/free-regular-svg-icons';
  import { faBoxOpen, faGamepad, faMagnifyingGlass, faTag, faUserGroup, faStar, faArrowDownAZ, faPlus, faDownload, faFire } from '@fortawesome/free-solid-svg-icons';
  library.add(faSteam, faBoxOpen, faGamepad, faUserGroup, faTag, faMagnifyingGlass, faStar, faCircleXmark, faArrowDownAZ, faPlus, faDownload, faFire);

  import VueSlider from 'vue-slider-component'
  import 'vue-slider-component/theme/default.css'
  import Tagify from '@yaireo/tagify'
  import '@yaireo/tagify/dist/tagify.css'

  import NavBar from '../components/NavBar.vue';
  import GameTile from '../components/GameTile.vue';

  // Variables
  // Auth
  const authStore = useAuthStore();
  const token = ref(authStore.token);

  // Filters
  let allGames = ref(null);
  let filteredGames = ref(null);
  let filteredSort = ref("Name");
  let filteredName = ref(null);
  let filteredPlatforms = ref(["Roblox", "Steam", "Party", "Other"]);
  let filteredPartySize = ref(0);
  let formattedFilteredPartySize = ref("Any");
  let filteredRating = ref(0.9);
  let formattedFilteredRating = ref("Any");
  let tagsWhitelist = ref([]);

  // Tagify
  const tagsTagify = ref(null);

  // Functions
  // Fetch data from api
  function fetchFromAPI(url) {
    return apiClient
    .get(url, {headers: { Authorization: `Token ${token.value}` },})
    .then((response) => response.data)
    .catch((error) => {console.error("Error fetching data:", error); throw error;});
  }
  
  // Filter games
  function filterGames() {
    if (!allGames.value) {
      return
    } else {
      // Collect tags
      let filteredTags = [];
      for (let tag of tagsTagify.value.value) {
        filteredTags.push(tag.value);
      }

      // Filter games
      filteredGames.value = allGames.value.filter(game => {

        // Define
        let matchName = true;
        let matchPlatform = true;
        let matchTags = true;
        let matchPartySize = true;
        let matchRating = true;

        // Match name
        try {matchName = game.name.toLowerCase().includes(filteredName.value.toLowerCase());} catch {matchName = true;}

        // Match platform
        try {matchPlatform = filteredPlatforms.value.includes(game.platform);} catch {matchPlatform = true;}

        // Match tags
        for (let tag of filteredTags) {
          if (game.tags.includes(tag)) {
            matchTags = true;
            break
          }
          matchTags = false;
        }

        // Match party size
        try {
          if (filteredPartySize.value != 0) {
            matchPartySize = filteredPartySize.value >= game.min_party_size && filteredPartySize.value <= game.max_party_size;
          } else {
            matchPartySize = true;
          }
        } catch {
          matchPartySize = true;
        }

        // Match rating
        try {
          if (filteredRating.value != 0.9) {
            matchRating = filteredRating.value <= game.average_rating;
          } else {
            matchRating = true;
          }
        } catch {
          matchRating = true;
        }

        return matchName && matchPlatform && matchTags && matchPartySize && matchRating;
      });

      // Sort filtered games
      if (filteredSort.value === "Average Rating") {
        filteredGames.value.sort((a, b) => b.average_rating - a.average_rating);
      } else if (filteredSort.value == "Popularity Score") {
        filteredGames.value.sort((a, b) => b.popularity_score - a.popularity_score);
      } else if (filteredSort.value === "Date Added") {
        filteredGames.value.sort((a, b) => new Date(b.date_added) - new Date(a.date_added));
      } else if (filteredSort.value === "Last Updated") {
        filteredGames.value.sort((a, b) => {
          const dateA = a.last_updated ? new Date(a.last_updated) : null;
          const dateB = b.last_updated ? new Date(b.last_updated) : null;

          if (!dateA && !dateB) return 0;
          if (!dateA) return 1;
          if (!dateB) return -1;

          return dateB - dateA;
        });
      } else {
        filteredGames.value.sort((a, b) => a.name.localeCompare(b.name));
      }
      
    }
  }

  // Update sliders if their values are changed
  watch(filteredPartySize, (newValue, oldValue) => {
    filterGames();
    if (newValue == 0) {
      formattedFilteredPartySize.value = "Any";
    } else {
      formattedFilteredPartySize.value = newValue;
    }
  });

  watch(filteredRating, (newValue, oldValue) => {
    filterGames();
    if (newValue == 0.9) {
      formattedFilteredRating.value = "Any";
    } else {
      formattedFilteredRating.value = newValue;
    }
  });

  // Toggle deselecting platform
  function toggleExcludePlatform(platform) {
    if (filteredPlatforms.value.includes(platform)) {
      filteredPlatforms.value = filteredPlatforms.value.filter(item => item !== platform);
    } else {
      filteredPlatforms.value.push(platform);
    }
    filterGames();
  }

  // Update sort type
  function updateSort(sortType) {
    filteredSort.value = sortType;
    filterGames();
  }

  // Clear filters
  function clearFilters() {
    filteredName.value = null;
    filteredPlatforms.value = ["Roblox", "Steam", "Party", "Other"];
    filteredPartySize.value = 0;
    formattedFilteredPartySize.value = "Any";
    filteredRating.value = 0.9;
    formattedFilteredRating.value = "Any";
    filteredSort.value = "Name";
    tagsTagify.value.removeAllTags();
    filterGames();
  }


  // Mounted
  onMounted(() => {
    // Get all games
    fetchFromAPI("/games/").then((data) => {allGames.value = data; filteredGames.value = data})

    // Create tags tagify
    let tagsInputElement = document.getElementById('gametags');
    tagsTagify.value = new Tagify(tagsInputElement, {maxTags: 5, whitelist: [], enforceWhitelist: true, dropdown: {enabled: 1, maxItems: 50, enabled: 0, closeOnSelect: false}});
    apiClient.get("/games/tags/", {headers: {Authorization: `Token ${token.value}`}})
    .then((response) => {
      for(let tag of response.data) {tagsWhitelist.value.push(tag["tag"])}
      tagsTagify.value.whitelist = tagsWhitelist.value
    })
    .catch((error) => {console.log(error)});

    tagsTagify.value.on('change', () => {
      filterGames();
    });
    
  });
</script>

<template>
  <NavBar />
  <div class="container-fluid">
    
    <h2 class="text-light py-2">All Games</h2>

    <div class="row">

      <div class="col-12 col-md-2">

        <p v-if="filteredGames">{{ filteredGames.length }} results found
        <span @click="clearFilters()" v-if="filteredName || 
                                            filteredPlatforms.length != 4 || 
                                            tagsTagify.value.length != 0 ||
                                            filteredPartySize != 0 ||
                                            filteredRating != 0.9 ||
                                            filteredSort != 'Name'" 
                                            class="badge bg-danger clearfilters">
                                            <font-awesome-icon icon="fa-regular fa-circle-xmark" /> 
                                            Clear filters
          </span>
        </p>

        <div class="row-12 dropdown">
          <button type="button" class="btn btn-secondary dropdown-toggle w-100 text-start" data-bs-toggle="dropdown">
            Sort by: 
            <font-awesome-icon v-if="filteredSort==='Name'" icon="fa-solid fa-arrow-down-a-z" />
            <font-awesome-icon v-if="filteredSort==='Popularity Score'" icon="fa-solid fa-fire" />
            <font-awesome-icon v-if="filteredSort==='Average Rating'" icon="fa-solid fa-star" />
            <font-awesome-icon v-if="filteredSort==='Date Added'" icon="fa-solid fa-plus" />
            <font-awesome-icon v-if="filteredSort==='Last Updated'" icon="fa-solid fa-download" />
            {{ filteredSort}}
          </button>
          <ul class="dropdown-menu w-100 bg-secondary">
            <li><a @click="updateSort('Name')" class="dropdown-item bg-secondary"><font-awesome-icon icon="fa-solid fa-arrow-down-a-z" /> Name</a></li>
            <li><a @click="updateSort('Popularity Score')" class="dropdown-item bg-secondary"><font-awesome-icon icon="fa-solid fa-fire" /> Popularity Score</a></li>
            <li><a @click="updateSort('Average Rating')" class="dropdown-item bg-secondary"><font-awesome-icon icon="fa-solid fa-star" /> Average Rating</a></li>
            <li><a @click="updateSort('Date Added')" class="dropdown-item bg-secondary"><font-awesome-icon icon="fa-solid fa-plus"/> Date Added</a></li>
            <li><a @click="updateSort('Last Updated')" class="dropdown-item bg-secondary"><font-awesome-icon icon="fa-solid fa-download" /> Last Updated</a></li>
          </ul>
        </div> 

        <p class="mt-2 mb-1">Filter platform</p>
        <div class="row-12 btn-group btn-group w-100">
          <button type="button" class="btn roblox" @click="toggleExcludePlatform('Roblox')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Roblox') }"> 
            <img src="/roblox.svg" alt="Roblox Logo" class="inline-svg">
          </button>
          <button type="button" class="btn steam" @click="toggleExcludePlatform('Steam')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Steam') }">
            <font-awesome-icon icon="fa-brands fa-steam" />
          </button>
          <button type="button" class="btn party" @click="toggleExcludePlatform('Party')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Party') }">
            <font-awesome-icon icon="fa-solid fa-box-open" />
          </button>
          <button type="button" class="btn other" @click="toggleExcludePlatform('Other')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Other') }">
            <font-awesome-icon icon="fa-solid fa-gamepad" />
          </button>
        </div>

        <div class="row-12">
          <p class="mt-1 mb-1">Filter name</p>
          <div class="input-group">
              <span class="input-group-text"><font-awesome-icon icon="fa-solid fa-magnifying-glass" /></span>
              <input v-if="filteredGames" v-model="filteredName" @input="filterGames()" class="form-control mainsearchbarquery" type="text" placeholder="Search">
              <input v-else class="form-control mainsearchbarquery" type="text">
          </div>
        </div>

        <div class="row-12">
          <p class="mt-2 mb-1">Filter tags</p>
          <div class="input-group">
            <span @click="filterGames()" class="input-group-text"><font-awesome-icon icon="fa-solid fa-tag" /></span>
            <input class="form-control tagifyinput mainsearchbarquery" id='gametags' name="gametags" placeholder="Search">
          </div>
        </div>

        <div class="row-12">
          <div class="mt-2 mb-1 d-flex justify-content-between">
              <span class="text-start"><font-awesome-icon icon="fa-solid fa-user-group" /> Party size: </span>
              <span class="text-end">{{ formattedFilteredPartySize }}</span>
            </div>
          <vue-slider 
              v-model="filteredPartySize"
              :min="0"
              :max="16"
              :interval="1"
              :adsorb="true"
              :contained="true"
              :tooltip="'none'"
            ></vue-slider>
        </div>

        <div class="row-12">
          <div class="mt-2 mb-1 d-flex justify-content-between">
              <span class="text-start"><font-awesome-icon icon="fa-solid fa-star" /> Min rating: </span>
              <span class="text-end">{{ formattedFilteredRating }}</span>
            </div>
          <vue-slider 
              v-model="filteredRating"
              :min="0.9"
              :max="10"
              :interval="0.1"
              :adsorb="true"
              :contained="true"
              :tooltip="'none'"
            ></vue-slider>
        </div>

      </div>

      <div class="col-12 col-md-10">
        <div v-if="filteredGames" class="row justify-content-start gx-2">
          <div v-for="game in filteredGames" class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2">
            <GameTile   v-if="filteredSort==='Average Rating'"
                        :name="game.name" 
                        :platform="game.platform" 
                        :install-size="game.install_size"
                        :link="game.link" 
                        :banner-link="game.banner_image_url" 
                        :date="game.last_updated"
                        date-text="Updated"
                        :tags="game.tags"
                        :min-party-size="game.min_party_size" 
                        :max-party-size="game.max_party_size"
                        :average-rating="game.average_rating"
                />
            <GameTile   v-else-if="filteredSort==='Date Added'"
                        :name="game.name" 
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
            <GameTile   v-else
                        :name="game.name" 
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
      </div>
    </div>
</div>

</template>

<style>

.mainsearchbar {
    flex-grow: 0;
    flex-basis: 50%;
}

input.mainsearchbarquery, input.mainsearchbarquery[type=text]{
    background-color: #505560;
    color: white;
    border: none;
    box-shadow: none !important;
    outline: none !important;
}

.roblox, .roblox:active {
  background: #e42818 !important;
}

.steam, .steam:active {
  background: #2a475e !important;
}

.party, .party:active {
  background: #4854f4 !important;
}

.other, .other:active {
  background: rgb(5, 88, 5) !important;
}

.roblox, .steam, .party, .other {
  color: #fff;
}

.excludedplatform {
  opacity: 50%;
}

span {
  color: #fff;
}

.dropdown-item {
  color: #f8f9fa;
  user-select: none;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f8f9fa !important;
  color: #000 !important;
}

.clearfilters {
  user-select: none;
  cursor: pointer;
}

</style>