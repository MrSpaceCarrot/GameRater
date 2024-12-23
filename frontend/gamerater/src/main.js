//import './assets/main.css'
import "bootstrap/dist/css/bootstrap.css";

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'

const loadConfig = async () => {
    const response = await fetch('/config.json');
    return await response.json();
}

const app = createApp(App);
app.use(router);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate)
app.use(pinia);

const config = await loadConfig();
app.provide('config', config)

app.mount('#app');

import "bootstrap/dist/js/bootstrap.js"
