<!-- This component is responsible for displaying a preview of a Sudoku
        - Filled numbers are blurred
        - When clicked, takes the user to play said puzzle
        - Keeps a savedPos as a prop to resume puzzle.
            - null if no puzzle has been saved -->
<template>
  <div>
    <!-- Displays puzzle information: name, author -->
    <div class="puzzle" v-on:click="goTo(puzzleName)">
      <p class="sudoku-name"> {{ this.puzzleName }} </p>
      <p class="sudoku-author"> Creator: {{ this.sudoku.author }} </p>
      <div class="sudoku" v-if="this.sudoku != null">

        <!-- Displays Sudoku grid -->
        <table v-if="this.savedPos == null">
          <tr class="sudoku-tr" v-for="(row, x) in this.sudoku.grid" :key="x">
            <td v-for="(col, y) in row" :key="y" class="sudoku-td">
              <div v-if="col != null" class="blur"> {{ col }} </div>
            </td>
          </tr>
        </table>
        <table v-else-if="this.sudoku!=[]">
          <tr class="sudoku-tr" v-for="(row, x) in this.savedPos" :key="x">
            <td v-for="(col, y) in row" :key="y" :class="[
              { 'sudoku-td': true },
              { 'isFromSaved': isFromSaved(x, y) }
            ]">
              {{ col }}
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../router";
import axios from "axios";
export default {
  name: "SudokuPreview",
  props: {
    puzzleName: String, //name of puzzle to preview
    miracle: Boolean, //true if puzzle is miracle sudoku
    savedPos: Array //null if savedPos doesn't exist, for resuming puzzles
  },
  data() {
    return {
      sudoku: [[]],
    };
  },
  created() {
    this.getPuzzle();
    this.startPos = this.savedPos;
  },
  methods: {
    // Gets puzzle data, excluding solution from db
    getPuzzle() {
      const path = this.$hostname + (this.miracle === true ? "/miracle-sudoku-puzzle?puzzleName=" : "/getpuzzle?puzzleName=") + this.puzzleName;
      axios
        .get(path)
        .then((res => {
          if (res) {
            this.sudoku = res.data;
            return;
          }
          else {
            alert("Puzzle could not be found!");
          }
        }))
        .catch((err) => {
          console.log("Puzzle " + this.puzzleName + " could not be found! " + err);
        });
    },
    // Returns true if number at coordinates (x,y) are from the savedPos
    isFromSaved(x, y) {
      if (this.sudoku.grid[x][y] == null) {
        if (this.savedPos[x][y] != null) {
          return true;
        }
      }
      return false;
    },
    // Routes user to play puzzle by name
    goTo(puzzleName) {

      router.push({
        name: "Play Sudoku",
        query: {
          puzzleName: puzzleName,
          miracle: this.miracle
        },
        params: { startPos: this.savedPos }
      })
    },
    // Returns number from (x,y) from savedPos
    getSavedCell(x, y) {
      try {
        return this.savedPos[x][y];
      } catch (err) {
        return null;
      }
    }
  },
};
</script>

<style scoped src="@/assets/styles/SudokuPreview.css"></style>
