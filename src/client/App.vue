<template>
  <div id="app">

    <h1>Barc Image Classifier</h1>

    <nav>
      <router-link to="/images">View Images</router-link>
      <router-link to="/objects">View Object List</router-link>
    </nav>

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

  #app > nav .router-link-active {
    display: none;
  }

  #app > nav {
    margin: 1rem 0;
  }

  a {
    text-decoration: none;
    color: #999;
  }

  a:hover {
    text-decoration: underline;
    color: inherit;
  }

</style>



