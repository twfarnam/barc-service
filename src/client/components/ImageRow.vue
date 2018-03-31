
<template>
  <div class=image>

    <div class=image-container>
      <div class=shim :style=shimStyle />
      <img :src=src />
    </div>

    <div class=data>

      <table v-if="image.result && image.result.length">
        <thead>
          <th>Classification</th>
          <th>Confidence</th>
        </thead>
        <tbody>
          <tr v-for="(row, i) in this.image.result"
            :class="{ spoken: i == 0 && row.confidence > .5 }">
            <td>{{ row.label }}</td>
            <td>{{ Math.round(row.confidence * 100) }}%</td>
          </tr>
        </tbody>
      </table>
      <div>No classifications</div>

      <div v-if=image.motion><b>Motion</b> {{ motion }}</div>
      <div class=time><b>Time</b> {{ time }}</div>
      <div v-if=image.ip_address><b>IP</b> {{ image.ip_address }}</div>
      <div v-if=image.device_id><b>Device ID</b> {{ image.device_id }}</div>

      <div class=categories>
        <div class=category v-for="(id) in this.image.categories">
          {{ labelForCategory(id) }}
          <span class="remove" @click="remove(id)">&times;</span>
        </div>
      </div>

      <select @change="add">
        <option value="">add category...</option>
        <optgroup v-for="(categories, room) in categoriesByRoom" :label="room">
          <option v-for="(object, id) in categories" :value="id">
            {{ object }}
          </option>
        </optgroup>
      </select>

    </div>

  </div>
</template>

<script>

export default {

  name: 'ImageRow',

  props: [ 'image', 'categories', 'addCategory', 'removeCategory' ],

  computed: {

    categoriesByRoom() {
      return this.categories.reduce((list, i) => {
        if (!this.image.categories.includes(i.id)) {
          list[i.room] = list[i.room] || { }
          list[i.room][i.id] = i.object
        }
        return list
      }, { })
    },

    time() {
      return (new Date(this.image.created_at)).toLocaleString()
    },

    src() {
      return `/static/images/${ this.image.id }.jpg`
    },

    shimStyle() {
      var aspect = this.image.height / this.image.width
      return `padding-top: ${ aspect * 100 }%`
    },

    motion() {
      const motion = this.image.motion
      const acceleration = Math.round(Math.max(
        Math.abs(motion.accelerationX),
        Math.abs(motion.accelerationY),
        Math.abs(motion.accelerationZ)
      ) * 100) / 100
      const rotation = Math.round(Math.max(
        Math.abs(motion.rotationX),
        Math.abs(motion.rotationY),
        Math.abs(motion.rotationZ)
      ) * 100) / 100
      return `${ rotation } rotation ${ acceleration } acceleration`
    },

  },

  methods: {

    labelForCategory(id) {
      const category = this.categories.find(i => i.id == id)
      return category.room + ': ' + category.object
    },

    add(event) {
      if (!event.target.value) return
      this.addCategory(this.image.id, event.target.value)
      event.target.value = ''
    },

    remove(id) {
      this.removeCategory(this.image.id, id)
    },

  },

}

</script>


<style scoped>

  .image {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-start;
    margin: 1rem 0;
  }

  .image-container {
    flex: 0 0 300px;
    position: relative;
    background: #ddd;
  }

  .image-container img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
  }

  .data {
    padding: 0 1rem;
  }

  .data > * {
    margin: 0.5em 0;
  }

  tr.spoken {
    font-weight: bold;
    color: red;
  }

  td {
    padding: 0 0.3em;
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

