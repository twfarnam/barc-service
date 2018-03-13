import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App'

Vue.config.productionTip = false

Vue.use(VueRouter)

var router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/:pageStart' },
  ],
})

new Vue({
  router,
  el: '#app',
  components: { App },
  template: '<App/>',
})

