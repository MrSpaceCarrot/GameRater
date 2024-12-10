<script>
  import axios from 'axios';

  import NavBar from '../components/NavBar.vue'

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faPencil } from '@fortawesome/free-solid-svg-icons';
  import { faGamepad } from '@fortawesome/free-solid-svg-icons';

  library.add(faSteam, faPencil, faGamepad);

  export default {
    name: 'Home',
    components: {
      NavBar,
      FontAwesomeIcon
    },
    data() {
      return {
        recentlyAddedGames: null,
        recentlyUpdatedGames: null
      };
    },
    mounted() {
      // Api Url
      const apiUrl = import.meta.env.VITE_API_URL;

      // Check if user is logged in
      const token = localStorage.getItem('token');
      if(!token) {this.$router.push({name: 'Login', params: { message: 'missingtoken'} });}
      axios.get(apiUrl + "/auth/verifytoken", {headers: {Authorization: `Token ${token}`}})
      .catch((error) => {this.$router.push({name: 'Login', params: { message: 'invalidtoken'} });});

      // Get recently added games
      this.fetchFromAPI(`${apiUrl}/games/recentadd`, token).then((data) => {this.recentlyAddedGames = data;})

      // Get recently updated games
      this.fetchFromAPI(`${apiUrl}/games/recentupdate`, token).then((data) => {this.recentlyUpdatedGames = data})
    },
    methods: {
      fetchFromAPI(url, token) {
        return axios
        .get(url, {headers: { Authorization: `Token ${token}` },})
        .then((response) => response.data)
        .catch((error) => {console.error("Error fetching data:", error); throw error;});
      },

      formatDate(date) {
        const givenDate = new Date(date);
        const currentDate = new Date();
        const difference = currentDate - givenDate;
        const daysDifference = Math.floor(difference / (1000 * 60 * 60 * 24));
        if (daysDifference == 0) {
          //const hoursDifference = Math.floor(difference / (1000 * 60 * 60));
          //return hoursDifference + " Hours ago"
          return "Today"
        } else {
          return daysDifference + " Days ago"
        }
      }
    }
  }
</script>

<template>
  <NavBar />
  <div class="container-fluid">
    <h2 class="text-light py-2">Home</h2>

    <!-- Recently added games -->
    <h5 class="text-light">Recently Added Games</h5>
    <div v-if="recentlyAddedGames" class="row justify-content-start">
      <div v-for="game in recentlyAddedGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 py-2">
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
            <p class="d-inline"> - </p>
            <p class="d-inline bg-success rounded date">{{ formatDate(game.date_added) }}</p>
            </p>
        </div>
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently added games -->

    <!-- Recently updated games -->
    <h5 class="text-light">Recently Updated Games</h5>
    <div v-if="recentlyUpdatedGames" class="row justify-content-start">
      <div v-for="game in recentlyUpdatedGames" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 py-2">
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
            <p class="d-inline"> - </p>
            <p class="d-inline bg-success rounded date">{{ formatDate(game.last_updated) }}</p>
            </p>
        </div>
      </div>
    </div>
    <p v-else>Loading...</p>
    <!-- /Recently updated games -->
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

.date {
  font-size: 0.8em;
  padding: 2px;
}

</style>