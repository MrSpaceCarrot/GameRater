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
    name: 'All',
    components: {
      NavBar,
      FontAwesomeIcon
    },
    data() {
      return {
        apiData: null,
      };
    },
    mounted() {
      const apiUrl = `${import.meta.env.VITE_API_URL}/games/`;

      axios.get(apiUrl)
      .then((response) => {
          this.apiData = response.data;
      })
      .catch((error) => {
          console.error('Error fetching data:', error);
      });
    },
    computed: {
      sortedApiData() {
        if(this.apiData) {
          return this.apiData.slice().sort((a, b) => a.name.localeCompare(b.name));
        };
      }
    }
  };
</script>

<template>

  <NavBar />

  <div class="container-fluid">
    <h2 class="text-light py-2">All Games</h2>

    <div v-if="apiData" class="row justify-content-start">
      <div v-for="game in sortedApiData" :key="game.id" class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 py-2">
          <div class="imgcontainer rounded">
            <a :href="game.link">
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