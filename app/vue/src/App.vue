<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <button v-on:click="spinnerToggle()"></button>
    <Spinner ref="spinner">
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Spinner from './components/Spinner.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    Spinner
  },
  methods: {
    spinnerToggle: function () {
      this.$refs.spinner.spinnerToggle();
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
