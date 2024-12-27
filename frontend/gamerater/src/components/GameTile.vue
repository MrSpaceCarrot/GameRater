<script setup>
  // Libraries & Components
  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faSteam } from '@fortawesome/free-brands-svg-icons';
  import { faBoxOpen, faGamepad, faHardDrive, faUserGroup, faStar} from '@fortawesome/free-solid-svg-icons';
  library.add(faSteam, faBoxOpen, faGamepad, faUserGroup, faHardDrive, faStar);

  // Props
  const props = defineProps(['name', 'platform', 'installSize', 'link', 'bannerLink', 'minPartySize', 'maxPartySize', 'tags', 'date', 'dateText', 'averageRating']);

  // Functions
  // Return difference between specified date and now
  function formatDate(date) {
    // Calculate difference
    const givenDate = new Date(date);
    const currentDate = new Date();
    const difference = currentDate - givenDate;
    const daysDifference = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hoursDifference = Math.floor(difference / (1000 * 60 * 60));
    const minsDifference = Math.floor(difference / (1000 * 60));

    // Format
    if (minsDifference < 60) {
      return `${minsDifference} mins ago`;
    } else if (hoursDifference == 1) {
      return `${hoursDifference} hour ago`;
    } else if (hoursDifference < 24) {
      return `${hoursDifference} hours ago`;
    } else if (daysDifference == 1) {
      return `${daysDifference} day ago`;
    } else {
      return `${daysDifference} days ago`;
    }
  }

  // Format party size
  function formatPartySize(minPartySize, maxPartySize) {
    if (minPartySize == maxPartySize) {
      return minPartySize;
    } else if (maxPartySize >= 16) {
      return `${minPartySize}+`;
    } else {
      return `${minPartySize} - ${maxPartySize}`;
    }
  }

  // Format install size
  function formatInstallSize(installSize) {
    if (installSize < 1) {
      return "<1 GB";
    } else {
      return `${installSize} GB`;
    }
  }
</script>

<template>
    <div class="gametilediv rounded">
        <div class="imgcontainer">
            <a :href="link" target="_blank">
                <img :src="bannerLink" :alt="`${name} banner image`" class="img-fluid hoverfade fixedsize">
            </a>
        </div>
        <div>
            <div class="text-center">
                <p class="text-light pt-1 mb-1">{{ name }}</p>
            </div>
        </div>
        <div class="mb-3">
            <p>
            <span v-if="platform === 'Roblox'" class="badge bg-danger">Roblox <img src="/roblox.svg" alt="Roblox Logo" class="inline-svg"></span>
            <span v-else-if="platform ==='Steam'" class="badge badge-steam">Steam <font-awesome-icon icon="fa-brands fa-steam" /></span>
            <span v-else-if="platform ==='Party'" class="badge badge-party">Party <font-awesome-icon icon="fa-solid fa-box-open" /></span>
            <span v-else-if="platform ==='Other'" class="badge badge-other">Other <font-awesome-icon icon="fa-solid fa-gamepad" /></span>

            <span v-if="minPartySize && maxPartySize" class="badge bg-primary"><font-awesome-icon icon="fa-solid fa-user-group" /> {{ formatPartySize(minPartySize, maxPartySize) }}</span>
            <span v-if="Number.isInteger(installSize)" class="badge bg-info"><font-awesome-icon icon="fa-solid fa-hard-drive" /> {{ formatInstallSize(installSize) }}</span>
            <span v-if="date" class="badge bg-success">{{ dateText }} {{ formatDate(date) }}</span>
            <span v-if="averageRating" class="badge bg-warning"><font-awesome-icon icon="fa-solid fa-star" /> {{ averageRating }}</span>

            <span v-for="tag in tags" class="badge bg-light text-dark fw-bolder">{{ tag }}</span>
            </p>
        </div>
    </div>
</template>

<style scoped>

.gametilediv {
  background-color: #49566b;
}

.date {
  color: #fff;
  font-size: 0.8em;
  padding: 2px;
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

.hoverfade {
    transition: all 0.2s ease-in-out 0s;
}

.hoverfade:hover {
    opacity: 0.5;
}

.badge-steam {
  background-color: #2a475e;
}

.badge-party {
  background: #4854f4;
}

.badge-other {
  background: rgb(5, 88, 5);
}

</style>