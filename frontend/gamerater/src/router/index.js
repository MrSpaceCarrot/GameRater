import { createWebHistory, createRouter } from 'vue-router'

import Home from '../views/Home.vue'
import All from '../views/All.vue'
import Add from '../views/Add.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/all/', component: All },
  { path: '/add/', component: Add },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router