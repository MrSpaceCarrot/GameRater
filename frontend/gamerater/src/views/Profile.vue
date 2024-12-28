<script setup>
  import NavBar from '../components/NavBar.vue';
  import { useAuthStore } from '@/stores/AuthStore';
  const authStore = useAuthStore();
</script>

<template>
<NavBar />
<div class="container d-flex flex-column justify-content-center position-absolute top-50 start-50 translate-middle text-center">

  <div class="d-inline-block">
      <img :src="authStore.avatar_link" class="bigusericon rounded-circle" alt="User Avatar">
  </div>

  <h4 class="text-light pt-1 pb-2">{{ authStore.display_name}}</h4>

  <ul class="nav nav-pills flex-column">
    <li class="nav-item">
      <div class="d-inline-block">
        <router-link to="/logout" class="nav-link text-light logoutbutton ms-2" href="">
            <p class="nav-link text-light bg-danger">Logout</p>
         </router-link>
      </div>
    </li>
  </ul>
</div>
</template>