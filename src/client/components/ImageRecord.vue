
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
        <div v-for="(category, index) in categories">
          {{ category }}
          <span class="remove" @click="removeCategory(index)">&times;</span>
        </div>
      </div>

      <select @change="change">
        <option>add category...</option>
        <option v-for="(category) in possible_categories">{{ category }}</option>
      </select>

    </div>
  </div>
</template>

<script>

import possible_categories from '../categories'

export default {

  name: 'App',

  props: [ 'image' ],

  computed: {

    date() {
      return (new Date(this.image.created_at)).toLocaleString()
    },

    src() {
      return `images/${ this.image.id }.jpg`
    },

    possible_categories() {
      return possible_categories.filter(c => !this.categories.includes(c))
    },

  },

  data: () => ({

    categories: [ ],

  }),

  methods: {

    removeCategory(index) {
      this.categories.splice(index, 1)
    },

    change(event) {
      this.categories.push(event.target.value)
      event.target.value = ''
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

  .remove {
    cursor: pointer;
  }

</style>

