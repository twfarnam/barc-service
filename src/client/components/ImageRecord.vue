
<template>
  <div class=image>
    <img :src="src">
    <div class=chatter>
      <div v-if=image.result class=result>{{ image.result }}</div>
      <div class=time>{{ date }}</div>
      <div v-if=image.latency>{{ image.latency }}ms</div>
      <div v-if=image.ip_address>IP: {{ image.ip_address }}</div>
      <div v-if=image.device_id>Device ID: {{ image.device_id }}</div>

      <div class=categories>
        <div class=category v-for="(category) in this.image.categories">
          {{ formatForLabel(category) }}
          <span class="remove" @click="remove(category)">&times;</span>
        </div>
      </div>

      <select @change="add">
        <option value="">add category...</option>
        <optgroup v-for="(categories, room) in categoryList" :label="room">
          <option v-for="(category) in categories" :value="category">
            {{ formatForSelect(room, category) }}
          </option>
        </optgroup>
      </select>

    </div>
  </div>
</template>

<script>

import { rooms, categories } from '../categories'
  
export default {

  name: 'App',

  props: [ 'image', 'addCategory', 'removeCategory' ],

  computed: {

    date() {
      return (new Date(this.image.created_at)).toLocaleString()
    },

    src() {
      return `images/${ this.image.id }.jpg`
    },

    categoryList() {
      return rooms.reduce((list, room) => {
        const roomCategories = categories.filter(cat =>
          cat.startsWith(room) &&
          !this.image.categories.includes(cat)
        )
        if (roomCategories.length)
          list[room.replace(/_/g,' ')] = roomCategories
        return list
      }, { })
    },

  },

  methods: {

    add(event) {
      this.addCategory(this.image.id, event.target.value)
      event.target.value = ''
    },

    remove(category) {
      this.removeCategory(this.image.id, category)
    },

    formatForSelect(room, category) {
      return category.slice(room.length + 1).replace(/_/g,' ')
    },

    formatForLabel(category) {
      return category.replace(/_/g,' ')
    },

  },

}

</script>


<style>

  .image {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-start;
    margin: 1rem 0;
  }

  .image img {
    width: 300px;
  }

  .image .chatter {
    padding: 0 1rem;
  }

  .categories {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-start;
    margin: 0.3em 0;
  }

  .category {
    margin: 0.3em 0;
    padding: 0.1em 0.3em;
    background: #eee;
    border: 1px solid #333;
    border-radius: 0.2em;
    text-transform: capitalize;
  }

  .remove {
    cursor: pointer;
    font-size: 1.3em;
    line-height: 0.5em;
  }

  select {
    font-size: 1.3em;
    text-transform: capitalize;
  }

</style>

