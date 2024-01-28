<!-- 200022530: A simple component for displaying a loading screen.
            Used by many components whilst retrieving data from the database.-->

<template>
    <div>
        <div class = "load-screen"></div>
        <h1 class = "load-notification"> Loading... </h1>
        <h2 class = "load-message" v-if = "this.message != null"> {{ message }}</h2>
    </div>
</template>

<script>
export default {
    name: "LoadScreen",
    props: {
        // Takes a message prop to be displayed underneath "Loading..."
        'message': String, 
    }
}
</script>

<styles scoped src = "@/assets/styles/LoadScreen.css">
</styles>