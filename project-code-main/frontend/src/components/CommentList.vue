<template>
  <div class="c">
    <div id="commentForm">
      <form @submit.prevent="doComment" class="w-100">
        <div class="form-group">
          <input type="text" name="commentArea" id="cmt" class="form-control" v-model="comment"
            placeholder="Add a comment..." />
          <button class="btn" id="sentButton"> Comment </button>
        </div>
      </form>
    </div>

    <div class="scroll" v-if="commentList.length != 0 || emptyComment">
      <div id="commentList">
        <p>Comments ({{ commentList.length }})</p>
        <ul v-if="!emptyComment">
          <li v-for="comment in commentList" :key="comment.id">
            <div class="comment">
              <div id="nd">
                <p id="account" v-on:click="goToAccount(comment.user)">{{ comment.user }}</p>
                <span id="date"> --{{ comment.date }}</span>
              </div>
              <p id="cmt-content">{{ comment.content }}</p>
              <p id="cmt-delete" v-on:click="deleteComment(comment)" v-if="hasDeletePermissions(comment)"> delete </p>
            </div>
          </li>
        </ul>
        <p v-else>There are no comments for now.</p>
      </div>
    </div>
    <div v-else>
      <LoadScreen message="Comments are loading." />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import LoadScreen from "./LoadScreen.vue";

export default {
  name: "CommentList",
  components: {
    LoadScreen,
  },
  props: {
    'puzzleName': String,
    'miracle': String,
  },
  data() {
    return {
      emptyComment: true,
      commentList: [],
      comment: "",
      role: "",
    };
  },
  created() {
    this.getComment();
    this.getUserRole(localStorage.getItem('username'));
  },
  methods: {
    getComment() {
      const path = this.$hostname + "/getComment?miracle=" + this.miracle + "&puzzleName=" + this.$route.query.puzzleName;
      axios
        .get(path)
        .then((res) => {
          this.commentList = res.data["comments"];
          this.puzzleId = res.data["id"];
          if (this.commentList.length !== 0) {
            this.emptyComment = false
          }
          this.$forceUpdate();
        })
    },
    getUserRole(user) {
      const path = this.$hostname + "/getuserrole?username=" + user;
      axios.get(path).then((res) => {
        this.userRole = res.data["role"];
      })
    },
    goToAccount(user) {
      this.$router.push("user?username=" + user);
    },
    sendComment(content) {
      const path = this.$hostname + "/comment?miracle=" + this.miracle + "&puzzleName=" + this.$route.query.puzzleName;
      if (!this.comment) {
        alert("Please add some comments")
      } else {
        axios.post(path, content)
          .then((res) => {
            switch (res.data['error']) {
              case '0':
                break;
              case '1':
                alert('An error occurred while commenting. Try again later!')
            }
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    commentInitialise() {
      this.comment = "";
      this.getComment();
      this.$forceUpdate();
    },
    doComment(e) {
      e.preventDefault();
      const content = {
        'user': localStorage.getItem('username'),
        'puzzleName': this.$route.query.puzzleName,
        'content': this.comment,
      };
      this.sendComment(content);
      this.commentInitialise();
      //TODO: get the new comment list
    },
    deleteComment(comment) {
      const path = this.$hostname + "/deletecomment?miracle=" + this.miracle + "&puzzleName=" + this.$route.query.puzzleName;
      axios.post(path, comment)
        .then((res) => {
          switch (res.data['error']) {
            case '0':
              break;
            case '1':
              alert('An error occurred while deleting comment. Try again later!')
          }
        })
        .catch((err) => {
          console.error(err);
        });
      if (this.commentList.length == 0) {
        this.emptyComment = true;
      }
      this.commentInitialise();
    },
    hasDeletePermissions(comment) {
      if (comment.user == localStorage.getItem('username')) {
        return true;
      } else if (this.userRole == "admin") {
        return true;
      }
      return false;
    }
  }
}


</script>
<style scoped src="@/assets/styles/CommentList.css"></style>