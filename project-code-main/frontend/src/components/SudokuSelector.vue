<!-- This component is responsible for displaying a selector for traditional and miracle sudokus
https://vuejs.org/guide/components/props.html#prop-validation
https://v2.vuejs.org/v2/guide/reactivity.html#Declaring-Reactive-Properties -->
<template>
  <div>
    <div class="container" v-if="puzzles.length != 0">

      <!-- Displays page title, sorting, and search options -->
      <div class="titles">
          <h3 v-if="showMiracleSudoku">Miracle Sudoku</h3>
          <h3 v-else>Traditional Sudoku </h3>
        <div class = "search-sort">
          <div>
            <input type="text" id="search" v-model="searchQuery" placeholder="Search puzzles by Name or Creator">
          </div>
          <div>
            <label for="sort">Sort by Difficulty: </label>
            <select id="sort" v-model="sortOrder">
              <option value="asc">Lowest to Highest</option>
              <option value="desc">Highest to Lowest </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Displays scrollmenu of Sudokus -->
      <!-- https://www.w3schools.com/howto/howto_css_menu_horizontal_scroll.asp -->
      <div class="scrollmenu">
        <div class="scrollmenu-item" v-for="puzzle in sortedPuzzles" :key="puzzle.id">
          <SudokuPreview 
            v-if = "puzzle.name != undefined"
            :puzzleName="puzzle.name"
            :miracle="showMiracleSudoku"
            :puzzleAuthor="puzzle.author"
            v-on:click="goTo(puzzle.name)">
          </SudokuPreview>
          <div class = "difficulty">
            <p>Difficulty Rating:</p>
            <star-rating class="star-rating-center" :rating="Number(puzzle.rating)" :read-only="true" :increment="0.1" v-bind:star-size="30" :active-color="['#ae0000','#FFFF00']" :active-border-color="['#F6546A','#a8c3c0']" :border-width="4" :star-points="[23,2, 14,17, 0,19, 10,34, 7,50, 23,43, 38,50, 36,34, 46,19, 31,17]" :active-on-click="false"></star-rating>
          </div>
        </div>
      </div>

    </div>
    <div v-else>
      <!-- Displays Load Screen if puzzle names are still being retrieved from database -->
      <LoadScreen
        message = "Puzzles are still loading"
      ></LoadScreen>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SudokuPreview from "./SudokuPreview.vue";
import LoadScreen from "./LoadScreen.vue";
import StarRating from 'vue-star-rating';

export default {
  name: "SudokuSelector",
  props:{
    miracle: Object, //True if showing miracle sudokus, otherwise null
  },
  components: {
    SudokuPreview,
    LoadScreen,
    StarRating
  },
  data() {
    return {
      id: 0,
      puzzles: [], //Stores puzzle names
      showMiracleSudoku: false, //True if showing miracle sudokus
      searchQuery: '',
      sortOrder: 'desc',
      sortOption: 'rating',
      author: '',
    };
  },
  created() { // Gets puzzle names from database
    if(this.miracle==true){
      this.showMiracleSudoku=true;
    }
    this.getPuzzles();
  },
  methods: {
    // Gets puzzle names to pass to SudokuPreview so they can be displayed
    getPuzzles() {
      let path = this.$hostname + (this.showMiracleSudoku?"/miracle-puzzle-names":"/puzzleNames");
      axios
        .get(path)
        .then((res) => {
          this.puzzles = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  computed: {
    filteredPuzzles() {
      if (this.searchQuery) {
        return Object.values(this.puzzles).filter(puzzle => 
          puzzle.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || puzzle.author.toLowerCase().includes(this.searchQuery.toLowerCase()));
      } else {
        return Object.values(this.puzzles);
      }
    },
    sortedPuzzles() {
      let sortedPuzzles = Object.values(this.filteredPuzzles);
      if (this.sortOrder === 'asc') {
        sortedPuzzles.sort((a, b) => a[this.sortOption] - b[this.sortOption]);
      } else {
        sortedPuzzles.sort((a, b) => b[this.sortOption] - a[this.sortOption]);
      }
      return sortedPuzzles;
    }
  }
};
</script>
<style scoped src = "@/assets/styles/SudokuSelector.css"/>
