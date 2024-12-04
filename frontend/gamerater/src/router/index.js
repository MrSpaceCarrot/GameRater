import { createWebHistory, createRouter } from 'vue-router'

import Home from '../views/Home.vue'

import Login from '../views/Login.vue'
import Logout from '../views/Logout.vue'
import AuthCallback from '../views/AuthCallback.vue'

import All from '../views/All.vue'
import Add from '../views/Add.vue'

import NotFound from '../views/NotFound.vue'

const routes = [
  { path: '/', name: "Home", component: Home },

  { path: '/login/:message?', name: "Login", component: Login },
  { path: '/logout', name: "Logout", component: Logout },
  { path: '/auth/callback', name: "AuthCallback", component: AuthCallback },

  { path: '/all/', name: "All", component: All },
  { path: '/add/', name: "Add", component: Add },

  { path: '/:pathMatch(.*)*', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

//router.beforeEach((to, from, next) => {
//  document.title = to.name + " | Derps Inc Gaming";
//  next();
//});

export default router