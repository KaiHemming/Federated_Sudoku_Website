<!-- This component is responsible for allowing users to create Sudokus and upload Sudokus that follow our federation's file format. -->
<template>
  <div>
    <div v-if="!isSubmitting">
      <!-- Description to indicate to user that they can change the type
            of Sudoku they are creating between Miracle and Traditional Sudoku. -->
      <p class = "description">
        <b>Note:</b> You can press the <b>switch button</b> to change the type of Sudoku created!
        <br/>
        We support Miracle and Traditional Sudoku.
        <br/><br/>
        Users can upload puzzles from other websites in the <b>Aces Supergroup Federation.</b>
      </p>

      <!-- Page Title: Type of Sudoku -->
      <div class="create-sudoku-title">
        <font-awesome-icon
          icon="fa fa-exchange-alt"
          style="margin-top: 1.6rem"
          class="miracle-toggle-button"
          @click="togglePage"
          title="Toggle between traditional and miracle sudokus"
        />
        <div v-if="showMiracleSudoku" style="padding: 10px">
          Create a Miracle Sudoku
        </div>
        <div v-else style="padding: 10px">Create a Sudoku</div>
      </div>

      <!-- Page Titles: Name of Sudoku and Creator -->
      <div class="puzzle">
        <h2 class="sudoku-title"> {{ sudokuName }}</h2>
        <body class = "creator" 
          v-on:click="goToAccount(username)"> 
            created by {{ username }}.
        </body>
        <div class = "container" style = "width: 30%">
          <input
            v-model="sudokuName"
            placeholder="Name your sudoku..."
          />

          <!-- Save and Upload buttons -->
          <font-awesome-icon icon="fa-regular fa-floppy-disk" class="save-button" style="margin-left:15px;" v-on:click="submit()"/>
          <div id="fileInputContainer">
            <label for="file-input">
              <!-- Uses same styling as download-button from PlaySudoku -->
              <font-awesome-icon icon="fa-solid fa-upload" class="download-button" style="margin-bottom:0; margin-left: 0"/>
            </label>
            <input id="file-input" type="file" ref="fileInput" @change="readFile" />
          </div>
        </div>
          <!-- Displaying the Sudoku 9 by 9 Grid -->
          <table class="sudoku" tabindex="0" @keydown="handleMoves">
            <tr class="sudoku-tr" v-for="(row, x) in sudoku" :key="x">
              <td
                v-for="(col, y) in row"
                :key="y"
                v-on:click="selectCell(x, y)"
                :class="[
                  { 'sudoku-td': true },
                  { isSelected: isSelected(x, y) },
                  { editible: col == null },
                ]"
              >
                {{ col }}
              </td>
            </tr>
          </table>
          <!-- Number selector for Mouse/Touchscreen controls -->
          <div class="number-selector">
            <button
              class="select-number-button"
              v-for="number in possibleNumbers"
              v-on:click="placeInCell(number)"
              :key="number"
            >
              <i v-if="number == null">
                <font-awesome-icon icon="fa-solid fa-eraser" />
              </i>
              {{ number }}
            </button>
          </div>
      </div>
    </div>
    <LoadScreen 
      v-else
      message = "Checking your puzzle, this may take a while..."
      />
  </div>
</template>

<script>
import axios from "axios";
import LoadScreen from "./LoadScreen.vue";

export default {
  name: "CreateSudoku",
  components: {
    LoadScreen,
  },
  data() {
    return {
      // Possible number selector for Standard Sudoku.
      possibleNumbers: [null, "1", "2", "3", "4", "5", "6", "7", "8", "9"],
      // Start with a blank Sudoku for the user to edit.
      sudoku: [
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
      ],
      // Currently selected cell defaults to 0,0 (The top left) for wasd controls.
      selectedCellX: 0,
      selectedCellY: 0,
      // Stores current Sudoku name to be sent to the backend.
      sudokuName: "Name Your Sudoku!",
      // Counts how many numbers have been placed for basic validity checks.
      counter: 0,
      showMiracleSudoku: false,
      gameType: "",
      username: localStorage.getItem("username"),

      // True if submitting puzzle, displays loadscreen if true
      isSubmitting: false
    };
  },
  created() {
    this.getRole();
  },
  destroyed() {
  },
  mounted() {
    const fileInput = document.getElementById("file-input");
    const customFileUpload = document.querySelector(".custom-file-upload");

    fileInput.addEventListener("change", function() {
    const filename = this.value.split("\\").pop();
    customFileUpload.textContent = filename;
});
  },
  methods: {
    // Redirects to user's account
    goToAccount(user) {
      this.$router.push("user?username=" + user);
    },
    // Gets role of the user
    getRole() {
      if (localStorage.getItem("role") == "player") {
        alert("You do not have the permissions to create a puzzle");
        this.$router.push({ name: "Home" });
        this.$router.go(0);
      }
    },
    // Changes type of Sudoku user is creating between Miracle and Traditional Sudoku
    togglePage() {
      this.showMiracleSudoku = !this.showMiracleSudoku;
    },
    // Allows users to upload Sudokus from other websites
    readFile(e) {
      const file = e.target.files;
      const reader = new FileReader();
      reader.onload = (e) => {
        const c = JSON.parse(e.target.result)
        try{
          this.sudoku = c['data']['puzzle']
        }catch(err){
          this.sudoku = c['puzzle']
        }
        try{
          this.sudokuName = c['name']
        }catch (err){
          //
        }
        this.username = c['author']['display_name']
        if(typeof this.username === 'undefined'){
          this.username = c['author']['username']
        }
      }
      reader.readAsText(file[0])
    },
    // Standard arrows keyboard controls.
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
      } else if (event.key === 'Backspace') {
        this.sudoku[this.selectedCellX][this.selectedCellY] = null;
        this.$forceUpdate();
      }
    },

    // Sends current Sudoku information to backend after performing the following initial checks:
    // - sudokuName field has been filled
    // - A minimum of 17 cells have been filled in the grid
    // The remainder of checks for a valid Sudoku are performed in the backend.
    // Then displays whether the Sudoku was successfully submitted or any relevant information to why it wasn't.
    submit() {
      this.isSubmitting = true;
      // Creating Sudoku: Name Checks
      if (this.sudokuName === "") {
        alert("Please name your Sudoku!");
        this.isSubmitting = false;
        return;
      } else if (!/^[a-zA-Z0-9_]+$/.test(this.sudokuName)) {
        alert("Invalid Sudoku name: Must only contain letters, numbers, and underscores!");
        this.isSubmitting = false;
        return;
      } else if (this.sudokuName.length < 5) {
        alert("Invalid Sudoku name: Must be at least 5 characters long!");
        this.isSubmitting = false;
        return;
      } else if (this.sudokuName.length > 40) {
        this.isSubmitting = false;
        alert("Invalid Sudoku name: Must be less than 41 characters long!");
        return;
      }

      // Set game type between either Traditional or Miracle Sudoku
      if (!this.showMiracleSudoku) {
        // Sudoku Validity (Simple Frontend check):
            // Has at least 17 cells filled
        this.counter = 0;
        for (const x in this.sudoku) {
          for (const y in this.sudoku) {
            if (this.sudoku[x][y] != null) {
              this.counter++;
            }
          }
        }
        if (this.counter < 17) {
          alert(
            "Careful, there are no valid sudokus with less than 17 cells filled!"
          );
          this.isSubmitting = false;
          return;
        }
        this.gameType = "Sudoku";
      } else {
        this.gameType = "MiracleSudoku";
      }

      // Submits sudoku to the backend to be checked
      axios
        .post(
          this.$hostname +
            (this.showMiracleSudoku
              ? "/create_sudoku/miracle"
              : "/create_sudoku"),
          {
            grid: this.sudoku,
            id: Math.ceil(Math.random() * 1000000),
            gameType: this.gameType,
            name: this.sudokuName,
            author: this.username
          }
        )
        .then((res) => {
          switch (res.data.error) {
            case "0":
              this.$router.push({ name: "Home" });
              this.$router.go(0);
              break;
            case "1":
              alert("Preexisting Sudoku Name: Please name your Sudoku something else");
              break;
            default:
              alert(res.data.error);
              break;
          }
          this.isSubmitting = false;
        });
    },
    // Changes selected cell coordinates
    selectCell(x, y) {
      (this.selectedCellX = x), (this.selectedCellY = y);
    },
    // Determines whether a cell has been selected using cell coordinates
    isSelected(x, y) {
      if (this.selectedCellX === x) {
        if (this.selectedCellY === y) {
          return true;
        }
      }
    },
    // Places a number in a given cell
    placeInCell(number) {
      this.sudoku[this.selectedCellX][this.selectedCellY] = number;
      // When placing an object performs two moves to ensure table updates.
      if (this.moveLeft()) {
        this.moveRight();
      } else {
        this.moveRight();
        this.moveLeft();
      }
    },

    // Moves selected cell up, down, left, or right for keyboard controls
    moveUp() {
      if (this.selectedCellX === 0) {
        return;
      } else {
        this.selectCell(this.selectedCellX - 1, this.selectedCellY);
      }
    },
    moveDown() {
      if (this.selectedCellX === 8) {
        return;
      } else {
        this.selectCell(this.selectedCellX + 1, this.selectedCellY);
      }
    },
    moveLeft() {
      if (this.selectedCellY === 0) {
        return false;
      } else {
        this.selectCell(this.selectedCellX, this.selectedCellY - 1);
        return true;
      }
    },
    moveRight() {
      if (this.selectedCellY === 8) {
        return;
      } else {
        this.selectCell(this.selectedCellX, this.selectedCellY + 1);
      }
    },
  },
};
</script>

<!-- Loads relevant CSS styling -->
<style scoped src="@/assets/styles/Sudoku.css">
</style>
