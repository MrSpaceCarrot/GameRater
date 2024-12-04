<script>
export default {
  name: 'AuthCallback',
  data() {
    return {
      loading: true,
      error: false,
    };
  },
  async created() {
    const code = new URL(window.location.href).searchParams.get("code");
    if (!code) {
      this.error = true;
      this.loading = false;
      return;
    }

    try {
    // Try get response from auth backend
      const response = await fetch(import.meta.env.VITE_API_URL + "/auth/discordcallback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ access_code: code })
      });
      // If no response is present, throw error
      if (!response.ok) throw new Error("Login failed");

      // Create token and redirect to home
      const data = await response.json();
      localStorage.setItem("token", data.token);
      this.$router.push('/');

    // Handle error and finished loading
    } catch (err) {
      console.error(err);
      this.error = true;
      this.$router.push({name: 'Login', params: { message: 'loginfail'} });
    } finally {
      this.loading = false;
    }
  }
};
</script>

<template>
  <div class="d-inline-flex m-3" v-if="loading">
    <div class="spinner-border text-light"></div>
    <p class="px-2">Logging in...</p>
  </div>
</template>