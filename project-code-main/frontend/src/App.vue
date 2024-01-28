<template>
  <div id="app">
    <router-view />
    <NavBar v-if="!$route.meta.hideNavBar" />
  </div>
</template>
<script>
import NavBar from "./components/NavBar.vue";

export default {
  name: "app",
  beforeCreate() {
    /*this.$store.commit("initialiseStore")

    const access_token = this.$store.state.access_token

    if(access_token){
      axios.defaults.headers.common['Authorization'] = "JWT " + access_token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }*/
  },
  components: {
    NavBar,
  },
};
</script>
<style scoped src="@/assets/styles/App.css"></style>
