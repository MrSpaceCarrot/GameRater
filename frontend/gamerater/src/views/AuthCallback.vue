<script setup>
  // Libraries & Components
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router'
  import axios from 'axios';
  import { useAuthStore } from '@/stores/AuthStore';

  // Variables
  const apiUrl = ref(import.meta.env.VITE_API_URL);
  const authStore = useAuthStore()
  const router = useRouter();

  const code = ref(new URL(window.location.href).searchParams.get("code"));

  // Mounted
  onMounted(() => {
    axios
    .post(apiUrl.value + "/auth/discordcallback", {access_code: code.value})
    .then((response) => {

      authStore.token = response.data.token;
      authStore.username = response.data.username;
      authStore.display_name = response.data.username;
      authStore.avatar_link = response.data.avatar_link;

      router.push('/');
    })
    .catch((error) => {
      router.push({ name: 'Login', params: { message: 'loginfail' } });
    });
  });
</script>

<template>
  <div class="d-inline-flex m-3">
    <div class="spinner-border text-light"></div>
    <p class="px-2">Logging in...</p>
  </div>
</template>