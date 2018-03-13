<template>
  <div id="app">

    <h1>Barc Image Classifier</h1>

    <pagination-links
      :prevLink=prevLink
      :nextLink=nextLink
    />

    <image-record
      v-for="(image) in images"
      :key=image.id
      :image=image
      :addCategory="addCategory"
      :removeCategory="removeCategory"
    />

    <pagination-links
      :prevLink=prevLink
      :nextLink=nextLink
    />

  </div>
</template>


<script>

import ImageRecord from './components/ImageRecord'
import PaginationLinks from './components/PaginationLinks'

export default {

  name: 'App',

  components: {
    ImageRecord,
    PaginationLinks,
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
      try {
        const response = await fetch(
          '/api/images?from=' + (this.$route.params.pageStart || 0),
          { credentials: 'same-origin' },
        )
        const { count, images } = await response.json()
        this.images = images.map(i => (i.categories = [ ], i))
        this.count = count
      }
      catch (error) {
        console.error(error)
        alert('An error has occurred. ' + error.message)
      }
    },

    addCategory(id, category) {
      const image = this.images.find(i => i.id === id)
      image.categories.push(category)
      this.saveImage(id)
    },

    removeCategory(id, category) {
      const image = this.images.find(i => i.id === id)
      image.categories = image.categories.filter(c => c != category)
      this.saveImage(id)
    },

    async saveImage(id) {
      try {
        const image = this.images.find(i => i.id === id)
        const response = await fetch('/api/images/' + id, {
          credentials: 'same-origin',
          method: 'PATCH',
          body: JSON.stringify(image),
          headers: { 'Content-Type' : 'application/json' }
        })
        const data = await response.json()
        console.log(data)
      }
      catch (error) {
        console.error(error)
        alert('An error has occurred. ' + error.message)
      }
    },

  }

}

</script>


<style>

  #app {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    padding-bottom: 3em;
  }

  a {
    text-decoration: none;
  }

</style>

