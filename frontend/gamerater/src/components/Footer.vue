<script setup>
    import { library } from '@fortawesome/fontawesome-svg-core';
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
    import { faGithub } from '@fortawesome/free-brands-svg-icons';
    library.add(faGithub);
</script>

<template>
<footer class="footer fixed-bottom bg-dark">
    <div class="container text-center my-0 py-0">
        <span class="text-white my-0 py-0">&COPY MrSpaceCarrot 2024</span>
    </div>
</footer>
</template>

<style scoped>
.p {
    margin: 0 !important;
    padding: 0;
}
</style>
