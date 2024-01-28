<template>
  <div class="container">
    <div class="login-title">Login</div>
    <form @submit.prevent="doLogin" class="w-100">
      <div class="form-group">
        <label>Username</label>
        <input
          type="username"
          class="login-custom-box"
          v-model="username"
          placeholder="Username"
        />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input
          type="password"
          class="login-custom-box"
          v-model="password"
          placeholder="Password"
        />
      </div>
      <button class="btn btn-primary btn-block login-button-style" id="login-button">Login</button>
      <div
        v-if="error"
        class="alert alert-warning alert-dismissable fade show mt-5"
        role="alert"
      >
        <strong>{{ error }}</strong>
      </div>
    </form>
    <div>
      <p class="login-question">
        New here? Click here to
        <router-link to="/register" style="color:#1abc9c; font-weight: bold">Register</router-link>
      </p>
      <p class="login-question">
        Forgot your password? Click here to
        <router-link to="/forgotPassword" style="color:#1abc9c; font-weight: bold">Reset your password</router-link>
      </p>
      <form @submit="sendToGroup" class="w-100">
        <p class="login-question">
          Or are you from our partner sites?
          <select name="group-names" id="group-names" class="supergroup-select" v-model="groupSelected">
            <option value="01">Group 1</option>
            <option value="02">Group 2</option>
            <option value="03">Group 3</option>
            <option value="04">Group 4</option>
            <option value="06">Group 6</option>
            <option value="07">Group 7</option>
            <option value="08">Group 8</option>
            <option value="09">Group 9</option>
          </select>
          <button class="btn btn-primary btn-sm login-button-style">Login</button>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    userLogin(content) {
      //const path = "/backend/login";
      const path = this.$hostname +"/login";
      if (!this.password) {
        this.error = "Please enter your password";
      } else if (!this.username) {
        this.error = "Please enter your username";
      } else {
        axios
          .post(path, content)
          .then((res) => {
            switch (res.data["error"]) {
              default: { // If not a number, the role of the user is stored.
                this.loggedIn = true;
                let name = content["username"];
                localStorage.setItem("loggedIn", this.loggedIn);
                localStorage.setItem("username", name);
                localStorage.setItem("role", res.data["error"]);
                this.$router.push({ name: "Home" });
                this.$router.go(0);
                break;
              }
              case "1":
                this.error = "Your username and password doesn't match";
                //setTimeout(() => this.$router.go(0) , 1000);
                break;
              case "2":
                this.error = "This user name isn't registered";
            }
            //this.$router.push({'name': 'Home'});
          })
          .catch((err) => {
            this.error = err;
            console.error(err);
            //setTimeout(() => this.$router.go(0) , 1000);
          });
      }
    },
    formInitialise() {
      this.username = "";
      this.password = "";
    },
    doLogin(e) {
      e.preventDefault();
      const content = {
        username: this.username,
        password: this.password,
      };
      this.userLogin(content);
      this.formInitialise();
    },
    sendToGroup(e) {
      e.preventDefault();
      const group_name = "group" + this.groupSelected;
      axios.post(this.$hostname+"/client_id_list", {"group_name":group_name}).then((response) => {
        this.client_id = response.data.client_id;
        window.location.href =
          "https://cs3099user" + this.groupSelected +
          ".host.cs.st-andrews.ac.uk/oauth/authorize?client_id=aces5&redirect_url=https%3A%2F%2Fcs3099user05.host.cs.st-andrews.ac.uk%2Foauth%2Fredirect%2F" +
          this.client_id; // When received, the receiver will append with their client_id.
      });
    },
  },
};
</script>

<style scoped src="@/assets/styles/Login.css">
</style>
