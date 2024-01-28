<template>
  <div>
    <div>
      <div id="title">
        <h3>Minesweeper</h3>
        <div id="mineNumber">
          <p>MineNumber: </p>
          <p id="n"> {{ this.mineNum }} </p>
        </div>

      </div>
    </div>
    <div id="menu">
      <button class="menu" v-if="isWin" v-on:click="getBoard()">😎</button>
      <button class="menu" v-if="!(isWin || isGameOver)" v-on:click="getBoard()">😃</button>
      <button class="menu" v-if="isGameOver" v-on:click="getBoard()">🥹</button>
      <p>Click to restart</p>
    </div>
    <div id="board">
      <table>
        <tbody>
          <tr v-for="(row, x) in board" :key="x">
            <td v-for="(col, y) in row" :key="y">
              <button class="minesweeper-button" v-bind:id="getCellID(x,y)" v-bind:class="[{ bomb: col.isMine },getAdjacentMines(x,y)]"  v-bind:disabled="col.isShown" v-on:click="showCell(x, y)" v-on:contextmenu.prevent="ToggleFlagCell(x,y)">{{ col.display }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

</template>

<script>
import axios from "axios";
import router from "@/router";

export default {
  name: "PlayMineSweeper",
  data(){
    return{
      mineNum: 0,
      rows:0,
      cols:0,
      board:[],
      grid:[],
      minePosition:[],
      isMine:false,
      isFlagged:false,
      isGameOver:false,
      isWin:false,
      isLose:false,
      check:true,
      cell:true,
      flag:true,

    }
  },
  created() {
    this.getBoard();
  },
  methods:{
    initializeGame(){
      for(let r=0; r<this.rows; r++){
        this.board[r] = [];
        for (let c=0; c<this.cols; c++){
          this.board[r][c] = {
          isMine: false,
          isFlagged: false,
          isShown: false,
          adjacentMines: this.grid[r][c],
          display:" "
          };
        }
      }
      for(let m= 0; m< this.minePosition.length; m++){
        let roww = this.minePosition[m][0];
        let coll = this.minePosition[m][1];
        this.board[roww][coll].isMine = true;
        this.board[roww][coll].adjacentMines = "0";

      }
      const container = document.getElementById("board");
      container.style.setProperty("--row", this.rows);
      container.style.setProperty("--col", this.cols);
    },
    getAdjacentMines(x,y){
      let classs = "adjacent_" + this.board[x][y].adjacentMines
      return classs
    },

    getBoard(){
      const diff = this.$route.query.difficulty
      let path=""
      if(diff !== "customise"){
        path = this.$hostname + "/getminesweeper?difficulty=" + diff
      }else{
        const rr = this.$route.query.row;
        const cc = this.$route.query.col;
        const mm = this.$route.query.mine;
        path = this.$hostname + "/getminesweeper?difficulty=" + diff+"&row=" +rr +"&col=" +cc +"&mine=" +mm;
      }
      axios
          .get(path)
          .then((res) => {
            this.grid = res.data["grid"]
            this.minePosition = res.data["minePosition"]
            this.rows = res.data['row'];
            this.cols = res.data['col'];
            this.mineNum = res.data['mines'];

            this.initializeGame();
            if(this.isWin || this.isGameOver) {
              this.gameStart();
              this.isWin = false;
              this.isLose = false;
              this.isGameOver = false;
            }
            this.$forceUpdate();
          })
    },

    showCell(r,c){
      let cell = this.board[r][c];
      if(cell.isFlagged){
        cell.isFlagged = false;
        this.mineNum += 1;
      }
      cell.isShown = true;
      if(cell.isMine){
        cell.display = "💣"
        this.isGameOver = true;
        let id = this.getCellID(r,c)
        let bt = document.getElementById(id);
        bt.classList.toggle("red");
        this.isLose = true;
        this.gameOver();
      }else{
        if(cell.adjacentMines !== "0" ){
          cell.display = this.grid[r][c];
        }
        this.$forceUpdate();
        if(cell.adjacentMines === "0"){
          this.showNeighbour(r,c);
        }
        this.checkWin();
        // if(this.isWin){
        //   setTimeout(
        //     function (){
        //       alert('YOU WIN!')
        //     },500);
        // }
        // this.$forceUpdate();
        // console.log(this.grid[r][c]);
        // console.log(cell)
      }

    },
    showNeighbour(r,c){
      let neighbourCell = [[r - 1, c - 1], [r - 1, c], [r - 1, c + 1],
                           [r, c - 1],                 [r, c + 1],
                           [r + 1, c - 1], [r + 1, c], [r + 1, c + 1]];
      let nr = 0
      let nc = 0
      // console.log("neighbourCell: " + neighbourCell)
      for(let i = 0; i < neighbourCell.length; i++){
        nr = neighbourCell[i][0];
        nc = neighbourCell[i][1];
          if ((nr >= 0 && nc >= 0) && (nr < this.rows && nc < this.cols)) {
            if(!this.board[nr][nc].isShown){
              this.showCell(nr,nc);
            }
          }
      }

    },
    ToggleFlagCell(r,c){
      if(!this.board[r][c].isShown){
        if (!this.board[r][c].isFlagged) {
          this.board[r][c].display = "🚩";
          this.board[r][c].isFlagged = true;
          this.mineNum -= 1;
        } else {
          this.board[r][c].display = " ";
          this.board[r][c].isFlagged = false;
          this.mineNum += 1;
        }
        console.log(this.board[r][c])
        this.checkWin();
        console.log(this.isWin)
        this.$forceUpdate();
      }
    },
    gameOver(){
      for(let a = 0; a < this.rows; a++){
        for(let b = 0; b < this.cols; b++){
          let id = a + "-" + b;
          const button = document.getElementById(id);
          this.board[a][b].isShown = true;
          if(this.board[a][b].isMine){
            this.board[a][b].display = "💣"
          }

          button.disabled = true;
        }
      }
      if(this.isWin){
         setTimeout(
            function (){
              alert('YOU WIN!')
            },500);
      };
      if(this.isLose){
         setTimeout(
            function (){
              alert('YOU LOSE!')
            },500);
      }
      this.$forceUpdate();
    },
    getCellID(r,c){
      return `${r}-${c}`;
    },
    checkWin(){
      this.check = true
      this.cell = true
      this.flag = true
      for(let k = 0; k < this.rows; k ++){
        for (let i = 0; i < this.cols; i++){
          if(this.board[k][i].isMine === false && this.board[k][i].isFlagged === true){
            this.flag = false
          }
        }
      }
      for (let k = 0; k < this.rows; k++) {
        for (let i = 0; i < this.cols; i++) {
          if (this.board[k][i].isMine === true && this.board[k][i].isFlagged === false) {
            this.check = false
            if (this.board[k][i].isMine === false && this.board[k][i].isFlagged === true) {
              this.check = false
            }
          }
        }
      }

      if (!this.check){
        for (let k = 0; k < this.rows; k++) {
          for (let i = 0; i < this.cols; i++) {
            if (this.board[k][i].isShown === false) {
              if(this.board[k][i].isMine === false){
              this.cell = false
              }
            }
          }
        }
      }
      if(this.flag){
        if (this.check || this.cell) {
          this.isWin = true
          this.gameOver();
        }
      }
      return this.isWin
    },
    gameStart(){
      for(let a = 0; a < this.rows; a++){
        for(let b = 0; b < this.cols; b++){
          let id = a + "-" + b;
          const button = document.getElementById(id);
          // console.log(id)
          button.disabled = false;
          // console.log(button)
        }
      }
      this.$forceUpdate();
    },
    goBack() {
      router.replace("/minesweeper")
    }
  },
}

</script>

<style scoped src="@/assets/styles/Minesweeper.css">

</style>