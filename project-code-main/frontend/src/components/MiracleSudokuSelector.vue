<template>
  <SudokuSelector :miracle="true"/>
</template>

<script>
import SudokuSelector from "./SudokuSelector"
export default {
  name: "MiracleSudokuSelector",
  components: {SudokuSelector}
}
</script>