
<template>
  <div class="links">
    <router-link v-if="prevLink" :to="prevLink">&larr; Previous Page</router-link>
    <router-link v-if="nextLink" :to="nextLink">Next Page &rarr;</router-link>
  </div>
</template>

<script>

module.exports = {

  props: [ 'nextLink', 'prevLink' ],

}

</script>

<style>

  a + a {
    margin-left: 3em;
  }

</style>

