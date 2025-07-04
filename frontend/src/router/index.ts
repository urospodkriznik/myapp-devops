import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Home from '@/views/Home.vue'
import Users from '@/views/Users.vue'
import Items from '@/views/Items.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  { 
    path: '/users', 
    component: Users,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  { 
    path: '/items', 
    component: Items,
    meta: { requiresAuth: true }
  },
  { 
    path: '/login', 
    component: Login,
    meta: { requiresGuest: true }
  },
  { 
    path: '/register', 
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/crypto-favorites',
    name: 'CryptoFavorites',
    component: () => import('../views/CryptoFavorites.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  
  // Try to refresh token if we have one but no user
  if (auth.token && !auth.user) {
    try {
      await auth.fetchMe()
    } catch (error) {
      // Token is invalid, clear it
      auth.token = ''
    }
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !auth.user) {
    next('/login')
    return
  }
  
  // Check if route requires admin access
  if (to.meta.requiresAdmin && auth.user?.role !== 'ADMIN') {
    next('/')
    return
  }
  
  // Check if route requires guest (not logged in)
  if (to.meta.requiresGuest && auth.user) {
    next('/')
    return
  }
  
  next()
})

export default router