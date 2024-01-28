<template>
  <nav class="navbar navbar-expand">
    <div class="container">
      <router-link to="/" class="navbar-brand">FPF</router-link>
      <div v-if="user">
        <!-- Produces a welcome message to the user if they're logged in. TODO: Limit size of username -->
        <!-- <router-link style="margin: 0" :to="accountPage" class="nav-link"> Welcome!</router-link> -->
      </div>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          <!-- https://stackoverflow.com/questions/60998519/adding-dropdowns-in-a-vue-js-router-link -->
          <!-- Loops through links to add to navigation bar -->
          <div class="row">
            <div class="nav-item" v-for="(link, index) in links" :key="index">
              <router-link
                :text="link.text"
                :key="link.text"
                :to="link.page"
                class="nav-link"> 
                {{ link.text }}
              </router-link>
            </div>
            <!-- Account dropdown menu -->
            <li class="nav-item dropdown" v-if="user">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                {{ username }}
              </a>
              <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                <p v-on:click="goToWithRefresh(accountPage)" class="dropdown-item">My Account</p>
                <li class="nav-item" @click="logoutMethod">
                  <router-link to="login" class="dropdown-item">Log out</router-link>
                </li>
              </div>
            </li>
            <!-- Links that are reliant on whether user is logged in are produced at the end-->
            <li class="nav-item" v-if="!user">
              <router-link to="login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item" v-if="!user">
              <router-link to="register" class="nav-link">Register</router-link>
            </li>
          </div>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import { RouterLink } from 'vue-router';
import router from "../router";

export default {
  name: "NavBar",
  data() {
      return {
          user: false,
          username: "",
          accountPage: "",
          // List of Links for navigation bar
          links: [
              {
                text: "Sudoku",
                page: "sudokus"
              },
              {
                text: "Miracle Sudoku",
                page: "miracle-sudokus"
              },
              {
                text:"Minesweeper",
                page:"minesweeper",
              },
              {
                text: "Create",
                page: "create"
              },
          ]
      };
  },
  methods: {
    // Logs out user
    logoutMethod() {
        if (this.user) {
            localStorage.clear();
            router.go('/login' );
           // this.$router.go(0);
        }
    },
    goToWithRefresh(link) {
      if (this.$route.name == "AccountPage") {
        router.push(link);
        router.go();
      } else {
        router.push(link);
      }
    }
  },
  // Determine whether user is logged in, if they're display a welcome message and correct navigation.
  mounted() {
    if (localStorage.getItem("loggedIn")) {
        let loggedIn = localStorage.getItem("loggedIn");
        this.user = loggedIn;
    }
    if (localStorage.getItem("username")) {
        let name = localStorage.getItem("username");
        // Sets username and account page url if user is logged in
        this.username = name;
        this.accountPage = "/user?username=" + name;
    }
  },
  components: { RouterLink }
};
</script>
<style scoped src="@/assets/styles/NavBar.css"></style>
