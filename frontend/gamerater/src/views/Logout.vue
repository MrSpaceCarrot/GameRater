<script setup>
  // Libraries & Components
  import { onMounted, ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/AuthStore';
  import apiClient from '@/axios';

  // Variables
  const route = useRoute();
  const router = useRouter();
  const authStore = useAuthStore();
  const token = ref(authStore.token);
  const type = ref(null);
  
  // Functions
  function logout() {

    type.value = route.params.type;
    if (type.value === "all") {
      apiClient.post("/auth/logoutall", {}, {headers: {Authorization: `Token ${token.value}`}})
    } else {
      apiClient.post("/auth/logout", {}, {headers: {Authorization: `Token ${token.value}`}})
    }
    
    authStore.token = null;
    authStore.username = null;
    authStore.display_name = null;
    authStore.avatar_link = null;

    router.push({ name: 'Login', query: { message: 'logout' } });
  }

  // Mounted
  onMounted(() => {
    
    logout()
  });
</script>

<template>
  <div class="d-inline-flex m-3">
    <div class="spinner-border text-light"></div>
    <p class="px-2">Logging out...</p>
  </div>
</template>