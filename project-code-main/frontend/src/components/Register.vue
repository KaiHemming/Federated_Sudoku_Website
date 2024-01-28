<template>
  <div class="container">
    <form @submit.prevent="doRegister">
      <div class="login-title">Register</div>
      <div class="form-group">
        <label>Username</label>
        <input type="username" class="login-custom-box" v-model="username" placeholder="Username" />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" class="login-custom-box" v-model="email" placeholder="email" />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" class="login-custom-box" v-model="password" placeholder="Password" />
      </div>
      <div class="form-group">
        <label>Confirm Password</label>
        <input type="password" class="login-custom-box" v-model="confirm_password" placeholder="Confirm Password" />
      </div>
      <div class="form-group">
        <label>Desired Role: </label>
        <!-- https://vuejs.org/guide/essentials/forms.html#radio -->
        <select v-model="role" class="supergroup-select">
          <option value="player">player</option>
          <option value="creator">creator</option>
        </select>
      </div>
      <button class="btn btn-primary btn-block" id="login-button">Register</button>
      <div v-if="error" class="alert alert-warning alert-dismissable fade show mt-5" role="alert">
        <strong>{{ error }}</strong>
      </div>
      <div>
        <p class="login-question">
          Already have an account? Click here to
          <router-link to="/login" style="color:#1abc9c; font-weight: bold">Login</router-link>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterPage",
  data() {
    return {
      //https://codepen.io/xichen/pen/EqWmza (6 line)
      rules: [
        { message: "One lowercase letter required.", regex: /[a-z]+/ },
        { message: "One uppercase letter required.", regex: /[A-Z]+/ },
        { message: "8 characters minimum.", regex: /.{8,}/ },
        { message: "One number required.", regex: /[0-9]+/ },
      ],
      username: "",
      password: "",
      confirm_password: "",
      error: "",
      email: "",
      role: "player",
    };
  },
  methods: {
    samePassword() {
      if (this.password !== this.confirm_password) {
        this.error = "Please enter the same password twice";
        return false;
      } else {
        return true;
      }
    },
    fieldChecks() {
      if (!this.username) {
        this.error = "Please enter a username";
        return false;
      } else {
        if (!this.password) {
          this.error = "Please enter a password";
          return false;
        } else if (!this.email) {
          this.error = "Please enter an email";
          return false;
        } else if (!this.confirm_password) {
          this.error = "Please confirm your password";
          return false;
        } else if (/\s/g.test(this.username)) {
          this.error = "A username cannot contain spaces! Please enter a valid username.";
          return false;
        } else if (!/^[a-zA-Z0-9_]+$/.test(this.username)) {
          this.error =
            "A username can only contain letters, numbers, and underscores! Please enter a valid username.";
          return false;
        } else {
          return true;
        }
      }
    },
    //https://codepen.io/xichen/pen/EqWmza (validation method)
    validation() {
      let errors = [];
      for (let condition of this.rules) {
        if (!condition.regex.test(this.password)) {
          errors.push(condition.message);
        }
      }
      if (errors.length === 0) {
        return true;
      } else {
        for (let err of errors) {
          this.error = err;
          return;
        }
      }
    },
    submittedUser(content) {
      const path = this.$hostname + "/register";
      if (
        this.fieldChecks() &&
        this.samePassword() &&
        this.validation()
      ) {
        axios
          .post(path, content)
          .then((res) => {
            if (res!=null) {
              switch (res.data["error"]) {
                case "0":
                  this.error = "Username already in use";
                  break;
                case "1":
                  this.$router.push({ name: "Login" });
                  break;
                case "2":
                  this.error = "Email already in use";
                  break;
              }
            }
          })
          .catch((err) => {
            this.error = err;
            console.error(err);
          });
      }
    },
    formInitialise() {
      this.username = "";
      this.password = "";
      this.confirm_password = "";
    },
    doRegister(e) {
      //this.error = "";
      e.preventDefault();
      const content = {
        username: this.username,
        password: this.password,
        confirm_password: this.confirm_password,
        email: this.email,
        role: this.role,
      };
      this.submittedUser(content);
      this.formInitialise();
    },
  },
};
</script>

<style scoped src="@/assets/styles/Login.css"></style>
