<script>
  import { library } from '@fortawesome/fontawesome-svg-core';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faDiscord } from '@fortawesome/free-brands-svg-icons';

  library.add(faDiscord);

  export default {
    name: 'Login',
    components: {
      FontAwesomeIcon
    },
    data() {
      return {
        message: this.$route.params.message
      }
    },
    mounted() {
      // Api Url
      //const apiUrl = import.meta.env.VITE_API_URL;
    },
    methods: {
      loginWithDiscord() {
        const clientId = import.meta.env.VITE_DISCORD_CLIENT_ID;
        const redirectUri = encodeURIComponent(import.meta.env.VITE_FINAL_REDIRECT_URI);
        const discordAuthUrl = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=identify`;
        window.location.href = discordAuthUrl;
      }
    }
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
                    <a class="nav-link text-light discordloginbutton" @click="loginWithDiscord">Login with Discord <font-awesome-icon icon="fa-brands fa-discord"/></a>
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