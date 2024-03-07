<template>
  <div id="app">
    <SfNavbar></SfNavbar>
    <router-view></router-view>
  </div>
</template>

<script>
import SfNavbar from './components/SfNavbar.vue';

export default {
  name: 'App',
  components: {
    SfNavbar,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
