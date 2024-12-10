<script setup>
  import { useAuthStore } from '@/stores/AuthStore';
  const authStore = useAuthStore();
</script>

<template>
<nav class="navbar navbar-expand-lg p-0">
    <div class="container-fluid bg-dark navbar-dark d-flex align-items-center">
        <div class="d-flex align-items-center flex-grow-1">

            <router-link to="/" class="navbar-brand" href="">
                <img src="/favicon.ico" alt="Site Logo" class="sitelogo">
            </router-link>

            <router-link to="/" class="text-light navbar-brand" href="all"><h2>Derps Inc Gaming</h2></router-link>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav d-flex align-items-center">
                    <li class="nav-item px-3">
                        <router-link to="/" class="nav-link nooverflow" href="">Home</router-link>
                    </li>
                    <li class="nav-item px-3">
                        <router-link to="/all" class="nav-link nooverflow" href="">All Games</router-link>
                    </li>
                    <li class="nav-item px-3">
                        <router-link to="/add" class="nav-link nooverflow" href="">Add Game</router-link>
                    </li>
                    <li class="nav-item px-3">
                        <router-link to="/top" class="nav-link nooverflow" href="">Top Rated</router-link>
                    </li>
                    <li class="nav-item px-3">
                        <router-link to="/rate" class="nav-link nooverflow" href="">Your Ratings</router-link>
                    </li>
                </ul>

                <!--

                <form class="d-flex input-group-sm mainsearchbar me-3">
                    <input class="form-control me-2 mainsearchbarquery" type="text" placeholder="Search">
                </form>

                -->
            </div>
        </div>

        <ul class="navbar-nav d-flex align-items-center">
            <li class="nav-item">
                <div class="d-flex align-items-center">
                    <router-link to="/profile" class="nav-link text-light" href="">
                        <img :src="authStore.avatar_link" class="usericon rounded-circle" alt="User Avatar">
                    </router-link>
                    <router-link to="/logout" class="nav-link text-light logoutbutton ms-2" href="">
                        <img src="/logout.svg" class="inline-svg">
                    </router-link>
                </div>
            </li>
        </ul>

    </div>
</nav>
</template>

<style>
.sitelogo {
    max-height: 50px;
    width: auto;
}

.usericon {
    max-height: 30px;
    width: auto;
}

.mainsearchbar {
    flex-grow: 0;
    flex-basis: 40%;
}

input.mainsearchbarquery, input.mainsearchbarquery[type=text]{
    background-color: #505560;
    color: white;
    border: none;
    box-shadow: none !important;
    outline: none !important;
}

.nooverflow {
    white-space: nowrap
}

.inline-svg {
    width: 1.1em;
    height: 1.1em;
    vertical-align: middle;
    margin-top: -3px;
}
</style>