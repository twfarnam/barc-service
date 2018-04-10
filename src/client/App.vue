<template>
  <div id="app">

    <h1>Barc Image Classifier</h1>

    <router-link to="/images">View Images</router-link>
    <router-link to="/categories">View Categories</router-link>

    <router-view />

  </div>
</template>


<script>

export default {

  name: 'App',

}

</script>


<style>

  #app {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    padding-bottom: 3em;
  }

  a {
    text-decoration: none;
    color: #999;
  }

  a:hover {
    text-decoration: underline;
    color: inherit;
  }

  .router-link-active {
    display: none;
  }

</style>

