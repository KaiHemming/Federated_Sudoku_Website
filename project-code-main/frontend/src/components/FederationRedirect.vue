<template>
  <div class="container">
    <!-- Displays a waiting message during redirect-->
    <h1>You are being redirected</h1>
    <p>Please Wait...</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RedirectPage",
  mounted() {
    const path = window.location.href;
    const client_id = path.replace("https://cs3099user05.host.cs.st-andrews.ac.uk/oauth/redirect/", "").split('?')[0];
    const code = this.$route.query.code;
    axios.post(this.$hostname+"/oauth/redirect/", {client_id: client_id, code: code}).then((res) => {
      localStorage.setItem("loggedIn", true);
      localStorage.setItem("role", "creator");
      localStorage.setItem("username", res.data.username);
      axios.post(this.$hostname+"/register-supergroup-user",{username: res.data.username} ).then({

      }).catch(error => console.log(error));
      this.$router.push({ name: "Home" });
      this.$router.go(0);
    }).catch(error => console.log(error));
  }
}
</script>
