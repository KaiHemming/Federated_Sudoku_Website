<template>
  <div class="container">
    <form @submit.prevent="doReset">
      <div class="login-title">Reset your password</div>
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
        <label>Email</label>
        <input
          type="email"
          class="login-custom-box"
          v-model="email"
          placeholder="email"
        />
      </div>
      <div class="form-group">
        <label>New Password</label>
        <input
          type="password"
          class="login-custom-box"
          v-model="password"
          placeholder="new password"
        />
      </div>
      <button class="btn btn-primary btn-sm login-button-style">Reset</button>
    </form>
    <div
        v-if="error"
        class="alert alert-warning alert-dismissable fade show mt-5"
        role="alert"
      >
        <strong>{{ error }}</strong>
      </div>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "ForgotPassword",
  data(){
    return{
      username:"",
      email:"",
      password:"",
      error:"",
      rules: [
        { message: "One lowercase letter required.", regex: /[a-z]+/ },
        { message: "One uppercase letter required.", regex: /[A-Z]+/ },
        { message: "8 characters minimum.", regex: /.{8,}/ },
        { message: "One number required.", regex: /[0-9]+/ },
      ],
    }

  },
  methods:{
    reset(content){
      const path = this.$hostname + "/reset";
      if(!this.password){
        this.error = "please enter your new password";
      }else if (!this.email){
        this.error = "please enter your email";
      }else if(!this.username){
        this.error = "please enter your username";
      }else if(this.validation()){
        axios
            .post(path, content)
            .then((res) => {
              switch (res.data['error']) {
                case "1":
                  this.error = "User detail does not match";
                  break;
                case "0":
                  this.$router.push({name: "Login"});
                  alert("reset password success")
                  break;
                case "2":
                  this.error = "`Your new password is the same as your old password";
                  break;

              }
            })
        .catch((err) => {
          this.error = err;
          console.error(err);
        });
      }else{
        // this.error = "invalid password";
      }
    },
    doReset(e){
      e.preventDefault();
      const content = {
        username: this.username,
        email: this.email,
        password: this.password,
      };
      this.reset(content);
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
          this.error += err;
        }
      }
    },

  },
}
</script>

<style scoped src="@/assets/styles/Login.css">
</style>