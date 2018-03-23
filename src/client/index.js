import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import ImageIndex from './components/ImageIndex.vue'

Vue.config.productionTip = false

Vue.use(VueRouter)

var router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/', redirect: '/images' },
    { path: '/images', component: ImageIndex },
  ],
  scrollBehavior(to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})

new Vue({
  router,
  el: '#app',
  components: { App },
  template: '<App/>',
})

