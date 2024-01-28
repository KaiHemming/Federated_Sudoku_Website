<template>
  <div class="container">
    <h3>Minesweeper Difficulty Selector</h3>
    <div id="selectMinesweeper">
      <div class="select" v-on:click="gotoEasy()">
        <p class="selectButton" v-on:click="gotoEasy()"> Easy </p>
      </div>
      <div class="select" v-on:click="gotoMedium">
        <p class="selectButton" v-on:click="gotoMedium"> Medium </p>
      </div>
      <div class="select" v-on:click="gotoHard">
        <p class="selectButton" v-on:click="gotoHard"> Hard </p>
      </div>
      <div class="select" v-on:click="showCustomise">
        <p class="selectButton" v-on:click="showCustomise"> Custom </p>
      </div>
    </div>
    <div class="customised" v-if="isCustomised">
      <p>Enter the number of row, columns, and mines:</p>
      <div class="input">
        <input
            id="row"
            placeholder="Number of rows"
            type="number"
            v-model="row"
        />
        <input
            id="col"
            placeholder="Number of columns"
            type="number"
            v-model="col"
        />
        <input
            id="mines"
            placeholder="Number of mines"
            type="number"
            v-model="mines"
        />
      <button v-on:click="gotoCustomise()">Generate</button>
      </div>
    </div>
  </div>
</template>

<script>
import router from "@/router";

export default {
  name: "MineSweeperSelector",
  data(){
    return {
      isCustomised: false,
      isEasy: false,
      isMedium:false,
      row:"",
      col:"",
      mines:""

    }
  },
  methods:{
    gotoEasy(){
      router.replace('/playMinesweeper?difficulty=easy')
    },
    gotoMedium(){
      router.replace('/playMinesweeper?difficulty=medium')
    },
    gotoHard(){
      router.replace('/playMinesweeper?difficulty=hard')
    },
    gotoCustomise(){
      if(this.row > 50 || this.col > 50){
        alert("Row and Column number should smaller than 50!")
        this.row = "";
        this.col = "";
        this.mines = "";
      }else if(this.row <= 0 || this.col <= 0|| this.mines <= 0 || this.mines>=(this.row*this.col)){
        alert("invalid board")
      }else {
        router.replace('/playMinesweeper?difficulty=customise&row=' + this.row + "&col=" + this.col + "&mine=" + this.mines)
      }
    },
    showCustomise(){
      this.isCustomised=true
    }
  }
}
</script>

<style scoped src="@/assets/styles/MinesweeperSelector.css">

</style>