
<template>
  <div class="links">

    <router-link v-if=prevLink :to=prevLink>
      &larr; Previous Page
    </router-link>
    <span v-else=prevLink />

    <span>
      Per Page:
      <select :value=meta.limit @change=changeLimit>
        <option>10</option>
        <option>50</option>
        <option>100</option>
        <option>500</option>
      </select>
    </span>

    <span>
      Sort:
      <select :value=meta.order @change=changeSort>
        <option value="created_at desc">Newest First</option>
        <option value="created_at asc">Oldest First</option>
      </select>
    </span>

    <router-link v-if=nextLink :to=nextLink>
      Next Page &rarr;
    </router-link>
    <span v-else=nextLink />

  </div>
</template>

<script>

export default {

  props: [ 'meta', 'change' ],

  computed: {

    nextLink() {
      const offset = this.meta.offset + this.meta.limit
      const link = this.stringifyQuery({ offset })
      return offset < this.meta.count ? link : false
    },

    prevLink() {
      const offset = Math.max(0, this.meta.offset - this.meta.limit)
      const link = this.stringifyQuery({ offset })
      return this.meta.offset > 0 ? link : false
    },

  },

  methods: {

    stringifyQuery(options) {
      const meta = Object.assign({}, this.meta, options)
      let query = [ ]
      if (meta.offset !== 0)
        query.push('offset=' + meta.offset)
      if (meta.order !== 'created_at desc')
        query.push('order=' + meta.order)
      if (meta.limit !== 10)
        query.push('limit=' + meta.limit)

      return query.length ? '?' + query.join('&') : ''
    },

    changeSort(event) {
      this.$router.push(this.stringifyQuery({
        offset: 0,
        order: event.target.value,
      }))
    },

    changeLimit(event) {
      this.$router.push(this.stringifyQuery({
        offset: 0,
        limit: event.target.value * 1,
      }))
    },

  },

}

</script>

<style scoped>

  .links {
    display: flex;
    flex-flow: row wrap;
    max-width: 800px;
  }

  .links > * {
    flex: 1 1 150px;
    margin: 0.3em 0.3em;
  }

</style>

