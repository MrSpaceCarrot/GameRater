<script setup>
  // Libraries & Components
  import { onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/AuthStore';

  // Variables
  const authStore = useAuthStore();
  const router = useRouter();

  // Functions
  function logout() {
    authStore.token = null;
    authStore.username = null;
    authStore.display_name = null;
    authStore.avatar_link = null;

    router.push({ name: 'Login', params: { message: 'logout' } });
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