<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <button v-on:click="spinnerToggle()"></button>
    <Spinner ref="spinner"> -->
    <div id="main-flame">

    </div>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
// import Spinner from './components/Spinner.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld,
    // Spinner
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
}

#main-flame {
  /* 画面の中心に来るように */
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);

  /* アスペクト比 16:9 */
  width: 80vw;
  height: calc(80vw * 0.5625);
  background-color: #8ff;

  /* 角を丸める */
  border-radius: 24px;
}
</style>
