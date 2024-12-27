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
  let userRatings = ref(null);
  let filteredSort = ref("Your Rating");

  // Functions
  // Fetch data from api
  function fetchFromAPI(url) {
    return axios
    .get(url, {headers: { Authorization: `Token ${token.value}` },})
    .then((response) => response.data)
    .catch((error) => {console.error("Error fetching data:", error); throw error;});
  }

  // Set alternating background colors
  function getBackground(index) {
    return index % 2 === 0 ? 'bglight' : 'bgdark';
  }

  // Update rating buttons for a specific game
  function updateRatingTile(gameId, rating) {

    // Get rating tile group and targeted rating
    const ratingTile = document.getElementById(`rating-${gameId}-${rating}`);
    const ratingGroup = document.getElementById(`ratinggroup-${gameId}`);

    // Reset all rating tile children to unselected value
    for (const childRatingTile of ratingGroup.children) {
      childRatingTile.classList.remove("btn-warning");
      childRatingTile.classList.add("btn-secondary");
    }

    // Set color of the selected rating tile
    ratingTile.classList.remove("btn-secondary");
    ratingTile.classList.add("btn-warning");
  }

  // Update all ratings buttons for all games
  function updateRatingTiles() {
    // For all games, check if user has rated them
    for (const game of allGames.value) {

      let ratingExists = false
      for(const rating of userRatings.value) {
        if (game.id === rating.game) {
          updateRatingTile(game.id, rating.rating);
          ratingExists = true;
          break;
        }
      }
      // Set default value if no rating exists
      if (!ratingExists) {
        updateRatingTile(game.id, 0);
      }
    }
  }

  // Submit rating to api and update UI
  function submitRating(gameId, rating) {

    // Create data object
    const data = {
      "game": gameId,
      "rating": rating
    };

    // Send request
    axios.post(apiUrl.value + "/ratings/add/", data, {headers: {Authorization: `Token ${token.value}`}})
    .then (() => {
      // Refresh user ratings
      fetchFromAPI(`${apiUrl.value}/ratings/user`).then((data) => {userRatings.value = data;})
      .then(() => {
        updateRatingTile(gameId, rating);
        updateSort(filteredSort.value);
      })
      .catch((error) => {
      console.error("Error getting ratings:", error);
      });
    })
    .catch((error) => {
      console.error("Error submitting rating:", error);
    });
  }

  // Update sort type
  function updateSort(sortType) {
    filteredSort.value = sortType;

    // Sort filtered games
    if (filteredSort.value === "Your Rating") {
      allGames.value.sort((a, b) => {
          const ratingA = userRatings.value.find(obj => obj.game === a.id)?.rating || null;
          const ratingB = userRatings.value.find(obj => obj.game === b.id)?.rating || null;

          if (ratingA === null && ratingB === null) return 0;
          if (ratingA === null) return -1;
          if (ratingB === null) return 1;

          return ratingB - ratingA;
        });
    } else {
      allGames.value.sort((a, b) => a.name.localeCompare(b.name));
    }
  }

  // Mounted
  onMounted(() => {
    // Get all games
    fetchFromAPI(`${apiUrl.value}/games/`).then((data) => {allGames.value = data;})

    // Get user ratings
    fetchFromAPI(`${apiUrl.value}/ratings/user`).then((data) => {userRatings.value = data;})
    .then(() => {
      updateRatingTiles();
      updateSort("Your Rating");
    });
  });
</script>

<template>
  <NavBar />
  <div class="container px-5">
    <h2 class="text-light py-2">Your Ratings</h2>

    <div class="row-12 dropdown mb-3">
      <button type="button" class="btn btn-secondary dropdown-toggle text-start" data-bs-toggle="dropdown">
        Sort by: {{ filteredSort}}
      </button>
      <ul class="dropdown-menu bg-secondary">
        <li><a @click="updateSort('Name')" class="dropdown-item bg-secondary">Name</a></li>
        <li><a @click="updateSort('Your Rating')" class="dropdown-item bg-secondary">Your Rating</a></li>
      </ul>
    </div> 

    <div v-if="allGames" class="row">
      <div v-for="(game, index) in allGames" :key="game.id" class="text-center pb-1" :class="getBackground(index)">

        <div class="row">
        
          <div class="col-12 col-md-6 d-flex align-items-center justify-content-start">
            <div class="aspect-ratio-box">
              <a :href="game.link" target="_blank">
                <img :src="game.banner_link" :alt="`${game.name} banner image`" class="img-fluid aspect-ratio-content rounded">
              </a>
            </div>
            <span class="px-3">{{ game.name }}</span>
          </div>

          <div class="col-12 col-md-6 d-flex align-items-center justify-content-end">
            <div class="nav-item ml-auto btn-group" :id="`ratinggroup-${game.id}`">
            <button @click="submitRating(game.id, 0)" type="button" :id="`rating-${game.id}-0`" class="btn btn-sm btn-secondary px-3">Haven't played</button>
            <button @click="submitRating(game.id, 1)" type="button" :id="`rating-${game.id}-1`" class="btn btn-sm btn-secondary px-3">1</button>
            <button @click="submitRating(game.id, 2)" type="button" :id="`rating-${game.id}-2`" class="btn btn-sm btn-secondary px-3">2</button>
            <button @click="submitRating(game.id, 3)" type="button" :id="`rating-${game.id}-3`" class="btn btn-sm btn-secondary px-3">3</button>
            <button @click="submitRating(game.id, 4)" type="button" :id="`rating-${game.id}-4`" class="btn btn-sm btn-secondary px-3">4</button>
            <button @click="submitRating(game.id, 5)" type="button" :id="`rating-${game.id}-5`" class="btn btn-sm btn-secondary px-3">5</button>
            <button @click="submitRating(game.id, 6)" type="button" :id="`rating-${game.id}-6`" class="btn btn-sm btn-secondary px-3">6</button>
            <button @click="submitRating(game.id, 7)" type="button" :id="`rating-${game.id}-7`" class="btn btn-sm btn-secondary px-3">7</button>
            <button @click="submitRating(game.id, 8)" type="button" :id="`rating-${game.id}-8`" class="btn btn-sm btn-secondary px-3">8</button>
            <button @click="submitRating(game.id, 9)" type="button" :id="`rating-${game.id}-9`" class="btn btn-sm btn-secondary px-3">9</button>
            <button @click="submitRating(game.id, 10)" type="button" :id="`rating-${game.id}-10`" class="btn btn-sm btn-secondary px-3">10</button>
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