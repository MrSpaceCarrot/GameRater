import { ref, computed } from "vue";
import { defineStore} from "pinia";

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    token: localStorage.getItem('token') || null,
    username: localStorage.getItem('username') || null,
    display_name: localStorage.getItem('display_name') || null,
    avatar_link: localStorage.getItem('avatar_link') || null
  }),
  persist: true,
});