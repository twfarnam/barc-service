<template>
  <div id="app">
    <h1>Barc Image Classifier</h1>

    <div class="links">
      <router-link v-if="prevLink" :to="prevLink">&larr; Previous Page</router-link>
      <router-link v-if="nextLink" :to="nextLink">Next Page &rarr;</router-link>
    </div>

    <image-record v-for="(image) in images" :key=image.id :image=image />

    <div class="links">
      <router-link v-if="prevLink" :to="prevLink">&larr; Previous Page</router-link>
      <router-link v-if="nextLink" :to="nextLink">Next Page &rarr;</router-link>
    </div>

  </div>
</template>


<script>

import ImageRecord from './components/ImageRecord'

export default {

  name: 'App',

  components: {
    ImageRecord,
  },

  data: () => ({
    pageSize: 10,
    count: null,
    images: [ ],
  }),

  computed: {

    pageStart() {
      return (this.$route.params.pageStart || 0) * 1
    },

    nextLink() {
      const next = this.pageStart + this.pageSize
      return next < this.count ? '/' + next : false
    },

    prevLink() {
      const prev = Math.max(0, this.pageStart - this.pageSize)
      return this.$route.params.pageStart > 0 ? '/' + prev : false
    },

  },

  mounted()  {
    this.fetch()
  },

  watch: {
    '$route'() { this.fetch() }
  },

  methods: {

    async fetch() {
      const response = await fetch(
        '/api/images?from=' + (this.$route.params.pageStart || 0),
        { credentials: 'same-origin' },
      )
      const { count, images } = await response.json()
      this.images = images
      this.count = count
    },

  }

}

</script>


<style>

  #app {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    padding-bottom: 3em;
  }

  .links a {
    text-decoration: none;
  }

  .links a + a {
    margin-left: 3em;
  }

</style>


