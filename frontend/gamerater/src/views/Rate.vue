<script setup>
  // Libraries & Components
  import { inject, ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/AuthStore';
  import axios from 'axios';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faBoxOpen, faGamepad, faHardDrive, faUserGroup} from '@fortawesome/free-solid-svg-icons';
  library.add(faSteam, faBoxOpen, faGamepad, faUserGroup, faHardDrive);
  
  import NavBar from '../components/NavBar.vue';

  // Variables
  const config = inject('config');
  const authStore = useAuthStore();
  const token = ref(authStore.token);
  const apiUrl = ref(config.API_URL);
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

        <div class="row">
        
          <div class="col-12 col-md-6 d-flex align-items-center justify-content-start">
            <div class="aspect-ratio-box">
              <a :href="game.link" target="_blank">
                <img :src="game.banner_link" :alt="`${game.name} banner image`" class="img-fluid aspect-ratio-content rounded">
              </a>
            </div>
            <span class="px-3">{{ game.name }}</span>
          </div>

          <!--
          <div class="col-12 col-md-2 d-flex align-items-center">
            <div>
              <span>Ratings</span>
            </div>
          </div>
          -->

          <div class="col-12 col-md-6 d-flex align-items-center justify-content-end">
            <div class="nav-item ml-auto btn-group">
            <button type="button" class="btn btn-sm btn-secondary px-3">1</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">2</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">3</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">4</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">5</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">6</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">7</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">8</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">9</button>
            <button type="button" class="btn btn-sm btn-secondary px-3">10</button>
              <!--
              <button type="button" class="btn btn-sm btn-danger">Terrible 🤮</button>
              <button type="button" class="btn btn-sm btn-danger">Bad 👎</button>
              <button type="button" class="btn btn-sm btn-danger">Eh 🙁</button>
              <button type="button" class="btn btn-sm btn-secondary">Neutral 😐</button>
              <button type="button" class="btn btn-sm btn-success">Ok 🙂</button>
              <button type="button" class="btn btn-sm btn-success">Good 👍</button>
              <button type="button" class="btn btn-sm btn-success">Peak 🔥</button>
               -->
            </div>
           
          </div>

        </div>
      </div>
    </div>
    <p v-else>Loading...</p>
</div>

</template>

<style scoped>

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
  max-width: 100%;
  height: auto;
}

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

.aspect-ratio-box {
  position: relative;
  height: 50px;
  width: 88.89px;
  overflow: hidden;
}

.aspect-ratio-content {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

</style>