<template>
  <div v-if="login === 'true'" class="container">
    <div class="leaderboard">
      <button class="close-button" @click="close">
        <font-awesome-icon icon="times" />
      </button>
      <h2 class="lb-section-title">{{ puzzleName }} Leaderboard</h2>
      <table class="table">
        <thead>
          <tr>
            <!-- table header -->
            <th>
              <div>Ranking</div>
            </th>
            <th>
              <div>Player Name</div>
            </th>
            <th>
              <div>Time</div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(player, index) in leaderboard.slice(0, 10)" :key="index" :class="{ 'highlighted': index === bestTimeIndex}">
            <td>{{ index + 1 }}</td>
            <td id="username" v-on:click="goToAccount(player.username)">{{ player.username }}</td>
            <td>{{ formatTime(player.time) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "LeaderboardFunction",
  props: {
    'puzzleID': Number,
  },
  data() {
    return {
      leaderboard: [],
      login: "",
      puzzleName: "",
      bestTimeIndex: -1,
    };
  },

  methods: {
    getLeaderBoard() {
      const path = this.$hostname + "/leaderboard?puzzleID=" + this.puzzleID;
      const namePath = this.$hostname + "/getpuzzlename?puzzleID=" + this.puzzleID;
      axios
        .get(namePath)
        .then((res) => {
          this.puzzleName = res.data.name;
        })
        .catch((err) => {
          console.error(err);
        });
      axios
        .get(path)
        .then((res) => {
          this.leaderboard = Object.entries(res.data.scores).map(([key, value]) => ({ id: key, ...value }));
          this.leaderboard.sort((a, b) => a.time - b.time);
          this.leaderboard.forEach((player, index) => player.ranking = index);
          this.bestTimeIndex = this.leaderboard.findIndex((player) => player.username === localStorage.getItem("username"))
          this.login = 'true';
        })
        .catch((err) => {
          console.error(err);
        });
    },
    close() {
      this.$emit("close");
    },
    goToAccount(username) {
      this.$router.push("user?username=" + username);
    },
  },
  created() {
    this.getLeaderBoard();
  },
  computed: {
    formatTime() {
      return (time) => {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
      };
    },
  },
};
</script>

<style scoped src="@/assets/styles/Leaderboard.css"/>
