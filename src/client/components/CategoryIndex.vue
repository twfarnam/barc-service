<template>
  <div>

    <div v-for="(room) in rooms" :key=room>

      <h2>{{ room }}</h2>

      <div class=objects>
        <div
          class=object
          v-for="(category) in categoriesByRoom(room)"
          :key=category.id>

          {{ category.object }}

          <img :src=src(category.id) />

        </div>
      </div>

    </div>

  </div>
</template>

<script>

export default {

  name: 'CategoryIndex',

  data: () => ({
    categories: [ ]
  }),

  mounted()  {
    this.fetchCategories()
  },

  computed: {

    rooms() {
      return this.categories.reduce((rooms, c) => {
        if (!rooms.includes(c.room)) rooms.push(c.room)
        return rooms
      }, [])
    }

  },

  methods: {

    categoriesByRoom(room) {
      return this.categories.filter(c => c.room == room)
    },

    src(id) {
      return `/static/categories/${ id }.jpg`
    },

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

  }

}

</script>

<style scoped>

  img {
    width: 200px;
  }

  .objects {
    display: flex;
    flex-flow: row wrap;
  }

  .object {
    display: flex;
    flex-flow: column nowrap;
    margin: 1rem;
    font-size: 1.3rem;
    font-weight: bold;
  }

</style>

