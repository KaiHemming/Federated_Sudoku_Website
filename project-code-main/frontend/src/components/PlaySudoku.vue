<!-- This component is responsible for allowing users to play Miracle and Traditional Sudokus on our website -->
<template>
  <div>
    <div class="puzzle" v-if="this.sudoku.length != 0">
      <div id="title">

        <!-- Displays puzzle information, e.g., name and ID -->
        <div class="id-name">
          <h2 class="sudoku-title">{{ this.sudoku.name }}</h2>

          <body class="creator" v-if="this.sudoku.author != null" v-on:click="goToAccount(sudoku.author)">
            created by {{ this.sudoku.author }}.
          </body>
          <p style="text-align:center" v-else>Author of puzzle couldn't be found.</p>
        </div>

      </div>
      <div class="timing-wrapper">
        <!-- Displays timer -->
        <div class="stopwatch" v-if="this.startPos == null">
          <span>{{ minutes }}</span>
          <span>:</span>
          <span>{{ seconds }}</span>
        </div>
        <div v-else>
          <p class="stopwatch" style="text-align:center"> Resumed Sudokus cannot be timed. </p>
        </div>
        <!-- Check Leaderboard -->
        <div>
          <button class="lbcheck" v-on:click="showLeaderboard = true">Check <br /> Leaderboard</button>
        </div>
      </div>

      <div id="content">
        <div id="puzzleArea">
          <!-- Displays Buttons: Hint, Pencil, Save, Download -->
          <div class="container">
            <div class="hint-container">
            <font-awesome-icon icon="fa-regular fa-lightbulb" class="hint-button" v-on:click="getHint()">
            </font-awesome-icon>
            <p class="hint-text" v-on:click="getHint()">{{ numberOfHintAvailable > 0 ? `Hint (+${(5 - numberOfHintAvailable) * 5}s)` : 'Hint' }}</p>
          </div>
          <font-awesome-icon icon="pencil-alt" :class="[{ 'pencil-button': true, 'pencil-on-color': this.pencilActive }]"
            v-on:click="() => { this.pencilActive = !this.pencilActive }" />
          <p>Pencil</p>
          <font-awesome-icon icon="fa-regular fa-floppy-disk" class="save-button" v-on:click="save()" />
          <p v-on:click="save()">Save</p>
          <font-awesome-icon v-if="miracle != 'true'" icon="fa-solid fa-download" class="download-button"
            v-on:click="download()" />
          <p v-if="miracle != 'true'" v-on:click="download()">Download</p>
        </div>

        <!-- Displays Sudoku grid -->
        <table
          v-bind:class="[{ 'sudoku': true }, { 'blur': !timerStarted && this.startPos == null }, { 'shake': isWrongNumber }]"
          class="sudoku" tabindex="0" @keydown="handleMoves">
          <tr class="sudoku-tr" v-for="(row, x) in this.sudoku.grid" :key="x">
            <td v-for="(col, y) in row" :key="y" :class="[
              { 'sudoku-td': true },
              { 'isSelected': isSelected(x, y) },
              { 'editible': isEditible(x, y) },
              { 'shake': isWrongNumber && isSelected(x, y) },
              { 'invalid': isInvalid(x, y) },
              { 'duplicate': isDuplicate(x, y) }
            ]" v-on:click="isEditible(x, y) && selectCell(x, y)">
              {{ col }}
              <table v-if="sudoku.grid[x][y] == null" class="small-grid">
                <tr class="pencil-tr" v-for="r in 3" :key="r">
                  <td class="pencil-td" v-for="c in 3" :key="c">
                    {{ annotations[x][y][r - 1][c - 1] }}
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>

        <!-- Number selector for Mouse/Touchscreen controls -->
        <div class="number-selector">
          <button class="select-number-button" v-for="number in possibleNumbers" v-on:click="placeInCell(number)"
            :key="number">
            <i v-if="number == null">
              <font-awesome-icon icon="fa-solid fa-eraser" />
            </i>
            {{ number }}
          </button>
        </div>

        <!-- Leaderboard overlay -->
        <div class="leaderboard-overlay" v-if="showLeaderboard">
          <Leaderboard :puzzleID="this.sudoku.id" @close="showLeaderboard = false" />
        </div>

      <!-- When finished solving puzzle, shows a custom alert box
                - Displays solve time
                    - Allows users to rate the puzzle's difficulty -->
        <div v-if="isSubmitted">
          <div v-if="showCustomAlert" class="custom-alert-box">
            <div class="custom-alert-content">
              <h1>Well Done!</h1>
              <p v-if="timerStarted">Your final time was: {{ minutes }} minutes and {{ seconds }} seconds!</p>
              <h2>Difficulty Rating:</h2>
              <star-rating class="star-rating-center" @rating-selected="setRating" :animate="true" v-bind:star-size="30"
                :active-color="['#ae0000', '#FFFF00']" :active-border-color="['#F6546A', '#a8c3c0']" :border-width="4"
                :star-points="[23, 2, 14, 17, 0, 19, 10, 34, 7, 50, 23, 43, 38, 50, 36, 34, 46, 19, 31, 17]"
                :active-on-click="false" :clearable="true"></star-rating>
              <button @click="submitRating">Submit</button>
            </div>
          </div>
        </div>

        <!-- Game over when ran out of lives -->
        <div v-if="gameOver">
          <div v-if="showCustomAlert" class="custom-alert-box">
            <div class="custom-alert-content">
              <h1>Game Over!</h1>
              <h2>You lost all three lives</h2>
              <button @click="refresh">Try Again</button>
            </div>
          </div>
        </div>

        <!-- When finished solving puzzle, if incorrect solve show game over -->
        <div v-if="incorrectSolution">
          <div v-if="showCustomAlert" class="custom-alert-box">
            <div class="custom-alert-content">
              <h1>Incorrect solution!</h1>
              <button @click="closeAlertBox">Close</button>
            </div>
          </div>
        </div>

        <!-- Starts playing a Sudoku, starts the timer which allows the cells to be edited. -->
        <div v-if="!this.playing">
          <button class="startButton" @click="startTimer()">
            Start!
          </button>
        </div>

        <star-rating class="star-rating-center" v-if="isRated" :rating="rating" :read-only="true" :animate="true"
          v-bind:star-size="30" :active-color="['#ae0000', '#FFFF00']" :active-border-color="['#F6546A', '#a8c3c0']"
          :border-width="4" :star-points="[23, 2, 14, 17, 0, 19, 10, 34, 7, 50, 23, 43, 38, 50, 36, 34, 46, 19, 31, 17]"
          :active-on-click="false" />
      </div>
      <div id="commentArea">
        <CommentList :puzzleName="this.$route.query.puzzleName" :miracle="this.miracle" ref="commentListRef" />
      </div>
    </div>
  </div>
  <div v-else>
    <LoadScreen message="Your puzzle will be ready shortly" />
  </div>
</div></template>

<script>
import axios from "axios";
import router from "../router";
import StarRating from 'vue-star-rating';
import CommentList from './CommentList.vue';
import LoadScreen from './LoadScreen.vue';
import Leaderboard from './Leaderboard.vue';

export default {
  name: "PlaySudoku",
  components: {
    StarRating,
    CommentList,
    LoadScreen,
    Leaderboard,
  },
  props: {
    startPos: Array
  },
  data() {
    return {
      sudoku: [], // Stores sudoku data
      annotations: Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => Array.from({ length: 3 }, () => Array.from({ length: 3 }, () => null)))),
      possibleNumbers: [null, "1", "2", "3", "4", "5", "6", "7", "8", "9"], //Possible numbers for numberSelector
      editibleCells: [], // Stores an array of coordinates for which cells are editable

      // Currently selected cell defaults to (0,0) - the top left, for keyboard controls.
      selectedCellX: 0,
      selectedCellY: 0,
      wrongNumber: 0,

      numEditibleCells: 0, // Keeps track of how many unfilled editible cells

      numberOfHintAvailable: 3,
      numberOfLives: 3,

      // These booleans are used to display different text boxes, divs, types of puzzles, etc.
      playing: false,
      pencilActive: false,
      miracle: false,
      isSubmitted: false,
      showCustomAlert: false,
      isRated: false,
      isWrongNumber: false,
      gameOver: false,
      incorrectSolution: false,
      timerStarted: false,

      // Variables submitted on completion of puzzle
      rating: 0,
      time: 0,
      showLeaderboard: false,
    };
  },
  created() {
    this.miracle = this.$route.query.miracle + "";
    // Retrieves specified sudoku from database using the puzzleName given as a query in the URL
    this.getPuzzle();
  },

  methods: {
    // Routes user to account page
    goToAccount(user) {
      this.$router.push("user?username=" + user);
    },
    // Gets puzzle from database
    getPuzzle() {
      const path = this.$hostname + (this.miracle == "true" ? "/miracle-sudoku-puzzle?puzzleName=" : "/getpuzzle?puzzleName=") + this.$route.query.puzzleName;
      axios
        .get(path)
        .then((res => {
          if (res) {
            this.sudoku = res.data;
            this.sudoku.name = this.$route.query.puzzleName;
          }
          else {
            alert("Puzzle could not be found!");
          }
        }))
        .catch((err) => {
          alert("Puzzle could not be found! " + err);
        });
    },
    // Refreshes page, used when retrying puzzle after game over
    refresh() {
      location.reload();
    },
    closeAlertBox() {
      this.showCustomAlert = false;
    },
    setRating(rating) {
      this.rating = rating;
    },
    showAlert() {
      this.showCustomAlert = true;
    },
    submitRating() {
      // send rating to backend
      const path = this.$hostname + "/sudoku/rating";
      axios.post(path, {
        name: this.sudoku.name,
        miracle: this.miracle,
        rating: this.rating
      })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error)
        });

      // ensures that user has rated the puzzle
      this.isRated = true;
      // closes alert box
      this.showCustomAlert = false;
      this.goBack();
    },
    // Goes back to SudokuSelector
    goBack() {
      router.replace("/sudokus")
    },
    // Standard WASD keyboard controls.
    // Additionally, hitting the enter key on the create Sudoku page attempts top submit the Sudoku
    handleMoves(event) {
      if (!isNaN(Number(event.key)) && event.key !== '0') {
        this.placeInCell(Number(event.key) + "");
      } else if (event.key === 'ArrowUp') {
        this.moveUp();
      } else if (event.key === 'ArrowLeft') {
        this.moveLeft();
      } else if (event.key === 'ArrowDown') {
        this.moveDown();
      } else if (event.key === 'ArrowRight') {
        this.moveRight();
      }
      event.preventDefault();
    },

    // Checks if a sudoku has been correctly solved, performs basic checks:
    // - Whether the grid has been filled
    // Then sends the solution to the backend to perform the remainder of checks.
    checkSolved() {
      this.playing = false;
      axios.post(this.$hostname + "/sudoku/check-full-solution", { name: this.sudoku.name, grid: this.sudoku.grid, miracle: this.miracle }).then(res => {
        if (res.data.message != "The solution is correct") {
          //If the sudoku hasn't been successfully solved
          this.incorrectSolution = true;
          this.showCustomAlert = true;
        } else {
          // Submits result to leaderboard
          if (localStorage.getItem('username') != this.sudoku.author) {
            axios.post(this.$hostname + "/leaderboard/submit", { username: localStorage.getItem('username'), time: this.time, puzzleID: this.sudoku.id })
          }
          else {
            alert("Puzzle Creators cannot submit scores!");
          }

          // If the sudoku has been successfully solved, cells can no longer be edited or selected.
          clearInterval(this.timer);
          this.timer = null;

          this.editibleCells = [];
          this.selectedCellX = null;

          //this.wrongAnswer = false;
          this.isSubmitted = true;
          this.incorrectSolution = false;
          this.showCustomAlert = true;
        }
      });
    },

    // Gets a hint from the backend.
    getHint() {
      if (this.playing) {
        this.numberOfHintAvailable -= 1
        if (this.numberOfHintAvailable < 0) {
          alert("You used all your hints!");
        }
        else {
          this.time += (4 - this.numberOfHintAvailable) * 5;
          axios.post(this.$hostname + "/sudoku/hint", { name: this.sudoku.name, grid: this.sudoku.grid, miracle: this.miracle }).then(res => {
            this.sudoku.grid = res.data.grid;
            this.numEditibleCells--;
            if (this.numEditibleCells == 0) {
              this.checkSolved();
            }
          });
        }
      }
    },

    // Selects a cell using coordinates
    selectCell(x, y) {
      if (this.selectedCellX != null) {
        (this.selectedCellX = x), (this.selectedCellY = y);
      }
    },

    // Determines whether a cell has been selected
    isSelected(x, y) {
      if (this.selectedCellX === x && this.selectedCellY === y) {
        return true;
      }
      return false;
    },

    // Checks solution after placing a number in a cell
    // If correct, does nothing
    // If incorrect, deducts life, shakes grid, removes entry
    checkPartialSolution(x, y) {
      axios.post(this.$hostname + "/sudoku/check-solution", { name: this.$route.query.puzzleName, grid: this.sudoku.grid, miracle: this.miracle }).then(res => {
        if (res.data.message !== "The solution is correct") {
          this.isWrongNumber = true;
          this.wrongNumber = this.sudoku.grid[x][y];

          setTimeout(() => {
            this.isWrongNumber = false;
          }, 500);

          this.numberOfLives -= 1;
          if (this.numberOfLives === 0) {
            this.gameOver = true;
            this.editibleCells = [];
            this.showCustomAlert = true;
            clearInterval(this.timer);
            this.timer = null;
          }

          setTimeout(() => {
            this.sudoku.grid[x][y] = null;
            this.numEditibleCells++;
          }, 200)
        } else {
          if (this.numEditibleCells == 0) {
            this.checkSolved();
          }
          else {
            console.log(this.numEditibleCells)
          }
        }
      });
    },

    // Places a number in a given cell
    placeInCell(number) {
      if (this.pencilActive == true) {
        if (this.isEditible(this.selectedCellX, this.selectedCellY)) {
          if (number == null) {
            for (let r = 0; r <= 2; ++r)
              for (let c = 0; c <= 2; ++c)
                this.annotations[this.selectedCellX][this.selectedCellY][r][c] = null;
          } else {
            if (this.annotations[this.selectedCellX][this.selectedCellY][Math.floor((number - 1) / 3)][(number - 1) % 3] == null)
              this.annotations[this.selectedCellX][this.selectedCellY][Math.floor((number - 1) / 3)][(number - 1) % 3] = number;
            else
              this.annotations[this.selectedCellX][this.selectedCellY][Math.floor((number - 1) / 3)][(number - 1) % 3] = null;
          }
        }
        this.$forceUpdate();
      }
      else if (this.sudoku != [[]]) {
        if (this.isEditible(this.selectedCellX, this.selectedCellY)) {
          if (number == null) {
            if (this.sudoku.grid[this.selectedCellX][this.selectedCellY] != null) {
              this.sudoku.grid[this.selectedCellX][this.selectedCellY] = null;
              this.numEditibleCells++;
            }
          } else {
            if (this.sudoku.grid[this.selectedCellX][this.selectedCellY] != number) {
              this.sudoku.grid[this.selectedCellX][this.selectedCellY] = number.toString();
              this.numEditibleCells--;
              this.checkPartialSolution(this.selectedCellX, this.selectedCellY);
            }
          }
          this.updateTable();
        }
      }
    },

    updateTable() {
      // When placing an object performs two moves to ensure table updates.
      if (this.moveLeft()) {
        this.moveRight();
      } else {
        this.moveRight();
        this.moveLeft();
      }
    },

    // Stores editible cells calculated from current grid state
    // Assumes filled in cells are correct.
    getEditibleCells() {
      for (const x in this.sudoku.grid) {
        for (const y in this.sudoku.grid) {
          if (this.sudoku.grid[x][y] == null) {
            this.editibleCells.push([x, y]);
            this.numEditibleCells++;
          }
        }
      }
      // When the editible cells are retrieved playing has started.
      this.playing = true;
    },
    // Determines whether cell coordinates are editible
    isEditible(x, y) {
      for (const cell in this.editibleCells) {
        if (this.editibleCells[cell][0] == x) {
          if (this.editibleCells[cell][1] == y) {
            return true;
          }
        }
      }
      return false;
    },

    // Moves selected cell up, down, left, or right for keyboard controls
    moveUp() {
      if (this.selectedCellX == 0) {
        return;
      } else {
        this.selectCell(this.selectedCellX - 1, this.selectedCellY);
      }
    },
    moveDown() {
      if (this.selectedCellX == 8) {
        return;
      } else {
        this.selectCell(this.selectedCellX + 1, this.selectedCellY);
      }
    },
    moveLeft() {
      if (this.selectedCellY == 0) {
        return false;
      } else {
        this.selectCell(this.selectedCellX, this.selectedCellY - 1);
        return true;
      }
    },
    moveRight() {
      if (this.selectedCellY == 8) {
        return;
      } else {
        this.selectCell(this.selectedCellX, this.selectedCellY + 1);
      }
    },
    download() {
      const path = this.$hostname + "/downloadPuzzle?puzzleName=" + this.$route.query.puzzleName
      axios
        .get(path, { responseType: 'blob' })
        .then((res) => {
          const url = window.URL.createObjectURL(new Blob([res.data]))
          const link = document.createElement('a')
          const fileName = this.$route.query.puzzleName + ".json"
          link.href = url
          link.setAttribute('download', fileName)
          document.body.appendChild(link)
          link.click()
        })
    },
    // Saves Sudoku's current solve state to user's account
    save() {
      if (this.playing) {
        const path = this.$hostname + "/saveposition";
        const username = localStorage.getItem("username");
        const sudoku = {
          'name': this.sudoku.name,
          'grid': this.sudoku.grid,
          'miracle': this.miracle
        }
        const content = {
          'username': username,
          'sudoku': sudoku,
        }
        axios
          .post(path, content)
          .then(alert("Position saved to your account!"))
          .catch((err) => {
            this.error = err;
            alert("Something went wrong! " + err);
          });
      }
    },
    /**
     * Starts the timer and changes the cells to editible.
     * Unblurs the cells.
     */
    startTimer() {
      this.getEditibleCells();
      if (this.startPos == null) {
        this.timerStarted = true;
        this.timer = setInterval(() => {
          this.time++;
        }, 1000);
      }
      else {
        this.populateWithSavedState();
      }

      document.querySelector('.sudoku').classList.remove('blur');
    },
    isInvalid(x, y) {
      if (this.isWrongNumber) {
        if (this.sudoku.grid[x][y] == this.wrongNumber) {
          return true;
        }
      }
      return false;
    },
    populateWithSavedState() {
      for (const x in this.sudoku.grid) {
        for (const y in this.sudoku.grid) {
          if (this.sudoku.grid[x][y] == null) {
            if (this.startPos[x][y] != null) {
              this.sudoku.grid[x][y] = this.startPos[x][y];
              this.numEditibleCells--;
            }
          }
        }
      }
    },
    isDuplicate(x, y) {
      if (this.playing) {
        if (this.sudoku.grid[x][y] == this.sudoku.grid[this.selectedCellX][this.selectedCellY]) {
          return true;
        }
      }
      return false;
    }
  },
  computed: {
    minutes() {
      const minutes = Math.floor(this.time / 60); // Computes the numnber of minutes
      return minutes < 10 ? "0" + minutes : minutes.toString(); // Adds a 0 if less than 10
    },
    seconds() {
      const seconds = this.time % 60; // Computes the number of seconds
      return seconds < 10 ? "0" + seconds : seconds.toString(); // Adds a 0 if less than 10
    },
  },
};
</script>

<!-- Loads relevant CSS styling -->
<style scoped src="@/assets/styles/Sudoku.css"/>
