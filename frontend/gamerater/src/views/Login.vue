<script setup>
  // Libraries & Components
  import { inject } from 'vue';
  import { useRoute } from 'vue-router';

  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faDiscord } from '@fortawesome/free-brands-svg-icons';
  library.add(faDiscord);

  // Variables
  const config = inject('config');
  const route = useRoute();
  const message = route.params.message;

  // Functions
  function loginWithDiscord() {
    const clientId = config.DISCORD_CLIENT_ID;
    const redirectUri = encodeURIComponent(config.LOGIN_REDIRECT_URL);
    const discordAuthUrl = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=identify`;
    window.location.href = discordAuthUrl;
  }
</script>

<template>
    <div class="container-fluid d-flex flex-column justify-content-center position-absolute top-50 start-50 translate-middle text-center">
        <div class="d-inline-block">
            <img src="/favicon.ico" class="bigusericon rounded-circle" alt="User Avatar">
        </div>

        <h2 class="text-light pb-4">Welcome to Derps Inc Gaming!</h2>

        <p v-if="message" class="red">Message: {{ message }}</p>

        <ul class="nav nav-pills flex-column">
            <li class="nav-item">
                <div class="d-inline-block">
                    <button @click="loginWithDiscord" class="btn btn-primary text-light discordloginbutton">Login with Discord <font-awesome-icon icon="fa-brands fa-discord"/></button>
                </div>
            </li>
        </ul>
    </div>
</template>

<style>

.discordloginbutton {
    background: #5865F2 !important;
}

.bigusericon {
    max-height: 100px;
    width: auto;
}

</style>