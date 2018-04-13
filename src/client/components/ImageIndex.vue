<template>
  <div>

    <pagination-links :meta=meta />

    <div class="loading" v-if="images.length === 0">Loading...</div>

    <image-row
      v-for="(image) in images"
      :key=image.id
      :image=image
      :categories=categories
      :addCategory=addCategory
      :removeCategory=removeCategory
      :deleteImage=deleteImage
    />

    <pagination-links :meta=meta />

  </div>
</template>

<script>

import ImageRow from './ImageRow.vue'
import PaginationLinks from './PaginationLinks.vue'

export default {

  name: 'ImageIndex',

  components: {
    ImageRow,
    PaginationLinks,
  },

  data: () => ({
    meta: {
      limit: 10,
      count: 0,
      offset: 0,
    },
    images: [ ],
    categories: [ ]
  }),

  mounted()  {
    this.fetchCategories()
    this.fetchImages()
  },

  watch: {
    '$route'() {
      this.images = [ ]
      this.fetchImages()
    }
  },

  methods: {

    async fetchCategories() {
      try {
        const response = await fetch(
          location.origin + '/api/categories',
          { credentials: 'same-origin' },
        )
        const { data } = await response.json()
        this.categories = data
      }
      catch (error) {
        console.error(error)
        alert('An error has occurred. ' + error.message)
      }
    },

    async fetchImages() {
      try {
        const response = await fetch(
          location.origin + '/api/images' + window.location.search,
          { credentials: 'same-origin' },
        )
        const { data, meta } = await response.json()
        this.images = data
        this.meta = meta
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

    removeCategory(image_id, category_id) {
      const image = this.images.find(i => i.id === image_id)
      image.categories = image.categories.filter(c => c != category_id)
      this.saveImage(image_id)
    },

    async saveImage(id) {
      try {
        const image = this.images.find(i => i.id === id)
        const endpoint = location.origin + '/api/images/' + id
        const response = await fetch(endpoint, {
          credentials: 'same-origin',
          method: 'PATCH',
          body: JSON.stringify(image),
          headers: { 'Content-Type' : 'application/json' }
        })
      }
      catch (error) {
        console.error(error)
        alert('An error has occurred. ' + error.message)
      }
    },


    async deleteImage(id) {
      const endpoint = location.origin + '/api/images/' + id
      const options = {
        credentials: 'same-origin',
        method: 'DELETE',
      }
      try {
        this.images = this.images.filter(i => i.id !== id)
        const response = await fetch(endpoint, options)
        this.fetchImages()

      }
      catch (error) {
        alert('delete error', error.message)
      }
    },

  }

}

</script>

<style scpoed>

  .loading {
    font-size: 4vw;
    min-height: 70vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

</style>


