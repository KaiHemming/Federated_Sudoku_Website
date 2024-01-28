<template>
  <div class="container">
    <h1>Login</h1>
    <form @submit.prevent="checkLogin" class="w-100">
      <!-- Username and Password form -->
      <div class="form-group">
        <label>Username</label>
        <input
          type="username"
          class="form-control"
          v-model="username"
          placeholder="Username"
        />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input
          type="password"
          class="form-control"
          v-model="password"
          placeholder="Password"
        />
      </div>
      <!-- Login button functionality implemented here -->
      <button class="btn btn-primary btn-block">Login</button>
      <div
        v-if="error"
        class="alert alert-warning alert-dismissable fade show mt-5"
        role="alert"
      >
        <strong>{{ error }}</strong>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      // Stores filled in form data
      username: "",
      password: "",
      // Stores any relevant login error messages
      error: "",
      client_id: "",
      // Redirection URL for successful login
      redirect_url: "",
    };
  },
  methods: {
    // Collects user login data from the backend
    userLogin(content) {
      const path = this.$hostname+"/federation_login";
      if (!this.password) {
        this.error = "Please enter your password";
      } else if (!this.username) {
        this.error = "Please enter your username";
      } else {
        axios
          .post(path, content)
          .then((res) => {
            switch (res.data["error"]) {
              case "0": { // On succesful login:
                let fullurl = window.location.href; // The user's current URL is stored.
                let args = fullurl.split("?")[1];
                let arg1 = args.split("&")[0];
                let arg2 = args.split("&")[1];

                this.redirect_url = arg2.split("=")[1];
                this.client_id = arg1.split("=")[1];
                alert("You are signing in from: " + this.client_id);
                axios.post(this.$hostname+"/generate-code", {"username":content.username, "client_id":this.client_id}).then(
                  (res) => {
                    const code = res.data.code // The access code contains an encrypted username and client_id.
                    window.location.href = decodeURIComponent(this.redirect_url) + "?code=" + encodeURIComponent(code);
                  });
                break;
              }
              case "1": // Unregistered user:
                this.error = "Your username and password doesnt match";
                break;
            }
          })
          .catch((err) => {
            this.error = err;
            console.error(err);
          });
      }
    },
    // Resets fields in form
    resetForm() {
      this.username = "";
      this.password = "";
    },
    // Checks user's form login details against details from the backend.
    checkLogin(e) {
      e.preventDefault();
      const content = {
        username: this.username,
        password: this.password,
      };
      this.userLogin(content);
      this.resetForm();
    },
  },
};
</script>
