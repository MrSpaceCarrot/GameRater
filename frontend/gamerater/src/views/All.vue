<script setup>
  // Libraries & Components
  import { ref, onMounted, watch } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import axios from 'axios';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faBoxOpen, faGamepad, faMagnifyingGlass, faTag, faUserGroup } from '@fortawesome/free-solid-svg-icons';
  library.add(faSteam, faBoxOpen, faGamepad, faUserGroup, faTag, faMagnifyingGlass);

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
  const apiUrl = ref(import.meta.env.VITE_API_URL);

  // Filters
  let allGames = ref(null);
  let filteredGames = ref(null);
  let filteredName = ref(null);
  let filteredPlatforms = ref(["Roblox", "Steam", "Party", "Other"]);
  let tagsWhitelist = ref([]);

  // Tagify
  const tagify = ref(null);
  let inputElement = ref(null);

  let marks = ref([1, 16]);

  // Functions
  // Fetch data from api
  function fetchFromAPI(url) {
    return axios
    .get(url, {headers: { Authorization: `Token ${token.value}` },})
    .then((response) => response.data)
    .catch((error) => {console.error("Error fetching data:", error); throw error;});
  }
  
  // Filter games
  function filterGames() {
    console.log("Filtering...");
    if (!allGames.value) {
      return
    } else {
      // Collect tags
      let filteredTags = [];
      for (let tag of tagify.value.value) {
        filteredTags.push(tag.value);
      }

      // Filter games
      filteredGames.value = allGames.value.filter(game => {

        // Define
        let matchName = true;
        let matchPlatform = true;
        let matchTags = true;

        // Match name
        try {
          matchName = game.name.toLowerCase().includes(filteredName.value.toLowerCase());
        } catch {
          matchName = true;
        }

        // Match platform
        try {
          matchPlatform = filteredPlatforms.value.includes(game.platform);
        } catch {
          matchPlatform = true;
        }

        // Match tags
        for (let tag of filteredTags) {
          if (game.tags.includes(tag)) {
            matchTags = true;
            break
          }
          matchTags = false;
        }

        return matchName && matchPlatform && matchTags;
      });
    }
  }

  // Toggle deselecting platform
  function toggleExcludePlatform(platform) {
    if (filteredPlatforms.value.includes(platform)) {
      filteredPlatforms.value = filteredPlatforms.value.filter(item => item !== platform);
    } else {
      filteredPlatforms.value.push(platform);
    }
    filterGames();
  }

  // Mounted
  onMounted(() => {
    // Get all games
    fetchFromAPI(`${apiUrl.value}/games/`).then((data) => {allGames.value = data; filteredGames.value = data})

    // Create tagify
    inputElement = document.getElementById('gametags');
    tagify.value = new Tagify(inputElement, {maxTags: 3, whitelist: [], enforceWhitelist: true, dropdown: {enabled: 1, maxItems: 50, enabled: 0, closeOnSelect: false}});

    // Get and set whitelist for tagify
    axios.get(apiUrl.value + "/tags", {headers: {Authorization: `Token ${token.value}`}})
    .then((response) => {
      for(let tag of response.data) {tagsWhitelist.value.push(tag["tag"])}
      tagify.value.whitelist = tagsWhitelist.value
    })
    .catch((error) => {console.log(error)});

    tagify.value.on('change', () => {
      filterGames();
    });
    
  });
</script>

<template>
  <NavBar />
  <div class="container-fluid">
    
    <h2 class="text-light py-2">All Games</h2>

    <div class="row">

       <div class="col-12 col-md-4 btn-group btn-group">
        <button type="button" class="btn roblox" @click="toggleExcludePlatform('Roblox')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Roblox') }">Roblox 
          <img src="/roblox.svg" alt="Roblox Logo" class="inline-svg">
        </button>
        <button type="button" class="btn steam" @click="toggleExcludePlatform('Steam')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Steam') }">Steam 
          <font-awesome-icon icon="fa-brands fa-steam" />
        </button>
        <button type="button" class="btn party" @click="toggleExcludePlatform('Party')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Party') }">Party 
          <font-awesome-icon icon="fa-solid fa-box-open" />
        </button>
        <button type="button" class="btn other" @click="toggleExcludePlatform('Other')" :class="{ 'excludedplatform': !filteredPlatforms.includes('Other') }">Other 
          <font-awesome-icon icon="fa-solid fa-gamepad" />
        </button>
      </div>

      <div class="col-12 col-md-4">
          <div class="input-group">
            <span @click="filterGames()" class="input-group-text"><font-awesome-icon icon="fa-solid fa-tag" /></span>
            <input class="form-control tagifyinput mainsearchbarquery" id='gametags' name="gametags">
          </div>
      </div>

      <div class="col-12 col-md-4">
        <div class="input-group">
            <span class="input-group-text"><font-awesome-icon icon="fa-solid fa-magnifying-glass" /></span>
            <input v-if="filteredGames" v-model="filteredName" @input="filterGames()" class="form-control mainsearchbarquery" type="text" :placeholder="`Search ${filteredGames.length} results`">
            <input v-else class="form-control mainsearchbarquery" type="text" placeholder="Search">
        </div>
      </div>

    </div>

    <div v-if="filteredGames" class="row justify-content-start">
      <div v-for="game in filteredGames" class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-2 py-2">
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
</div>

</template>

<style scoped>

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

.roblox {
  background: #e42818;
}

.steam {
  background: #2a475e;
}

.party {
  background: #4854f4;
}

.other {
  background: rgb(5, 88, 5);
}

.roblox, .steam, .party, .other {
  color: #fff;
}

.excludedplatform {
  opacity: 50%;
}

</style>