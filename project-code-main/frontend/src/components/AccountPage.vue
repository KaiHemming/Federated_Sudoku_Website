<!-- 200022530: This component is responsible for displaying relevant information to a user.
                - Interfaces with PlaySudoku to resume puzzles saved to accounts
             -->

<template>
    <div class="container" v-if="isLoaded()">
        <!-- Shows User information:
                - Account name
                - User's role
                -  -->
        <div class="user-info-wrapper">
            <div class= "basic-info">
                <h3 v-if = "this.user.username != null"> {{ this.user.username }}'s Account 
                    <p v-if = "this.user.role != null"> {{ this.user.role }}</p>
                    <p class="promote-button" v-if = "this.canPromote" v-on:click = "promote()">Promote</p>
                </h3>
            </div>
            <p></p>
            <div class = "bio">
                <p v-if = "this.bio != null">
                    "{{ this.bio }}"
                </p>
                <p v-else> This user has not saved a bio. </p>
                <div class = "edit-bio">
                    <p 
                        class = "edit-button" 
                        v-on:click = "editingBio = true"
                        v-if="!editingBio && isCurrentUser()"> 
                            Edit Bio</p>
                    <input 
                        v-if="editingBio" 
                        class = "edit-bio-textbox" 
                        v-model="bio" 
                        v-on:keyup.enter="saveBio()"/>
                    <p
                        class = "edit-button"
                        v-on:click = "saveBio()"
                        v-if="editingBio">
                            Save </p>
                </div>
            </div>
        </div>
        <!-- Displays sudoku saved to account if:
                - The account matches the current user
                - The user has saved a sudoku-->
        <div class = "saved-sudoku-wrapper">
            <div class = "saved-sudoku-instructions">
                <h3>How to save Sudokus</h3>
                <p>
                    Registered users can resume playing sudokus if they have saved them. <br/>
                    However, timer and leaderboard features will be unavailable. <br/>
                    If a user has saved a sudoku position, it will be seen on the right.
                </p>
            </div>
            <div class = "currentlyPlaying" v-if = "this.savedPuzzle != null">
                <h3>Saved Sudoku</h3>
                <p>Resume playing Sudokus from any point in a solve!</p>
                <SudokuPreview 
                    v-if = "this.savedPuzzle.name != undefined && isCurrentUser()"
                    :savedPos = "this.savedPuzzle.grid"
                    :puzzleName="this.savedPuzzle.name"
                    :miracle="this.savedPuzzle.miracle==='true'">
                </SudokuPreview>
                <h2 v-else-if="!isCurrentUser()"> You cannot view saved puzzle states of other users! </h2>
                <h2 v-else > You have not saved a puzzle! </h2>
            </div>
            <div v-else class = "currentlyPlaying">
            <p> No saved puzzle. </p>
            </div>
        </div>
    </div>
    <!-- Displays a loadscreen whilst getting data from database -->
    <LoadScreen 
        v-else
        message = "User account is loading"
        />
</template>
<script>
import router from "../router";
import axios from "axios";
import SudokuPreview from "./SudokuPreview.vue";
import LoadScreen from "./LoadScreen.vue";

export default {
    name: "AccountPage",
    components: {
        SudokuPreview,
        LoadScreen,
    },
    data() {
        return {
            user: [], //stores user data
            bio: "This user has no bio.",   //default bio message will 
                                            //be replaced when user data is loaded
            savedPuzzle: [],
            loadedSudoku: false, // true when sudoku data is loaded
            loadedUser:false, // true when user data is loaded
            editingBio:false, // true whilst user is editing bio
            canPromote: false // true if current user can promote this account to admin
        }
    },
    mounted() {
        this.getUserData();
        this.getSavedSudoku();
    },
    methods: {
        // Gets user data using username query in URL
        // If corresponding user data does not exist,
        //      Alerts the user and then sends them back to the home page
        getUserData() {
            const path = this.$hostname + ("/getuserdata?username=") + this.$route.query.username;
            axios
                .get(path)
                .then((res => {
                if (res) {
                    this.user = res.data;
                    this.userRole=res.data["role"]
                }
                else {
                    alert("User could not be found!");
                }
                }))
                .then(() => {
                    this.loadedUser = true;
                    this.bio = this.user.bio;
                    this.isPromotePossible();
                })
                .catch(() => {
                alert("User could not be found! Redirecting to home page");
                router.push("/home");
                });
        },
        // Gets saved sudoku using username query in URL
        //      Once loaded sets loadedSudoku to true to move past the load screen
        getSavedSudoku() {
            const path = this.$hostname + ("/getsaveposition?username=") + this.$route.query.username;
            axios
                .get(path)
                .then((res => {
                if (res) {
                    this.savedPuzzle = res.data;
                }}))
                .then(this.loadedSudoku = true)
        },
        // Sends edited bio to backend to update database, reloads page after saving
        // If user attempts to save an empty bio
        //      Replaces bio with "This user has no bio."
        saveBio() {
            if (this.bio != "") {
                this.postBio({
                    'username': localStorage.getItem("username"),
                    'newBio': this.bio,
                })
            }
            else {
                this.postBio({
                    'username': localStorage.getItem("username"),
                    'newBio': null,
                })
            }
        },

        // Posts bio to backend
        postBio(content) {
            const path = this.$hostname + "/postbio"
            axios
                .post(path, content)
                .then(alert("Saved new bio! Reloading Page!"))
                .catch(err => {
                    this.error = err;
                    alert("Something went wrong! " + err);
                })
            this.editingBio= false;
            this.$router.go(); //reloads page
        },
        // Returns true when both user and sudoku data has been loaded
        isLoaded() {
            if (this.loadedUser && this.loadedSudoku == true) {
                return true;
            }
            return false;
        },
        // Returns true if user account page matches current user
        isCurrentUser() {
            if (localStorage.getItem("username") == this.user.username) {
                return true;
            }
            return false;
        },
        // Returns true if a user can be promoted by current user
        isPromotePossible() {
            const path = this.$hostname + "/getuserrole?username=" + localStorage.getItem("username");
            axios.get(path).then((res) => {
                this.userRole = res.data["role"];
                if (this.user.role != "admin" && res.data["role"] == 'admin') {
                    this.canPromote = true;
                }
            })
        },
        // Promotes user to admin
        promote() {
            const path = this.$hostname + "/promote?username=" + this.user.username;
            axios.post(path).then(router.go());
        }
    }
}
</script>
<style scoped src="@/assets/styles/AccountPage.css">
</style>