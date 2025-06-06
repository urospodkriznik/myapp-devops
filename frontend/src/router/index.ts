import { createRouter, createWebHistory } from 'vue-router'
import Users from '../views/Users.vue'
import Items from '../views/Items.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/users' },
    { path: '/users', component: Users },
    { path: '/items', component: Items }
  ]
})

export default router