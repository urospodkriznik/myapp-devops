import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persistedstate'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

import axios from 'axios'
import { useAuthStore } from './stores/auth'

const vuetify = createVuetify({
  icons: { defaultSet: 'mdi', aliases, sets: { mdi } }
})

const pinia = createPinia()
pinia.use(piniaPersist)

const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(vuetify)

axios.defaults.withCredentials = true

axios.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

axios.interceptors.response.use(undefined, async (error) => {
  const auth = useAuthStore()
  if (
    error.response &&
    error.response.status === 401 &&
    !error.config.url?.includes("/login")
  ) {
    try {
      await auth.refresh()
      error.config.headers.Authorization = `Bearer ${auth.token}`
      return axios.request(error.config)
    } catch {
      auth.logout()
      window.location.href = "/login"
    }
  }
  return Promise.reject(error)
})

app.mount('#app')