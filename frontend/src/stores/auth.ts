import { defineStore } from 'pinia'
import axios from 'axios'
import { useNotificationStore } from './notifications'

interface User {
  id: number
  name: string
  email: string
  role: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: '' as string,
    user: null as User | null,
    loading: false as boolean,
  }),
  persist: true,
  actions: {
    async login(email: string, password: string) {
      const notifications = useNotificationStore()
      this.loading = true
      
      try {
        const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/login`, { 
          email, 
          password 
        }, { 
          withCredentials: true 
        })
        
        this.token = res.data.access_token
        await this.fetchMe()
        notifications.success('Successfully logged in!')
        return true
      } catch (error: any) {
        console.error('Login error:', error)
        
        if (error.response?.status === 401) {
          notifications.error('Invalid email or password. Please try again.')
        } else if (error.response?.status === 422) {
          notifications.error('Please check your input and try again.')
        } else if (error.code === 'NETWORK_ERROR') {
          notifications.error('Network error. Please check your connection.')
        } else {
          notifications.error('Login failed. Please try again later.')
        }
        
        return false
      } finally {
        this.loading = false
      }
    },
    
    async register(name: string, email: string, password: string) {
      const notifications = useNotificationStore()
      this.loading = true
      
      try {
        await axios.post(`${import.meta.env.VITE_API_BASE_URL}/register`, { 
          name, 
          email, 
          password 
        })
        
        notifications.success('Registration successful! Please log in.')
        return true
      } catch (error: any) {
        console.error('Registration error:', error)
        
        if (error.response?.status === 400) {
          const detail = error.response.data?.detail
          if (typeof detail === 'string') {
            notifications.error(detail)
          } else {
            notifications.error('Registration failed. Please check your input.')
          }
        } else if (error.code === 'NETWORK_ERROR') {
          notifications.error('Network error. Please check your connection.')
        } else {
          notifications.error('Registration failed. Please try again later.')
        }
        
        return false
      } finally {
        this.loading = false
      }
    },
    
    async fetchMe() {
      if (!this.token) return
      
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/me`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        this.user = res.data
      } catch (error: any) {
        console.log("fetchMe failed, clearing user")
        this.user = null
        this.token = ''
        
        // Don't show notification for token expiration during app load
        if (error.response?.status === 401) {
          // Silent token refresh attempt
          try {
            await this.refresh()
          } catch {
            // Token refresh failed, user needs to login again
          }
        }
      }
    },
    
    async refresh() {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/refresh`, { 
          withCredentials: true 
        })
        this.token = res.data.access_token
        await this.fetchMe()
        return true
      } catch (error) {
        console.log("refresh failed")
        this.token = ''
        this.user = null
        throw new Error("refresh failed")
      }
    },
    
    logout() {
      const notifications = useNotificationStore()
      
      this.token = ''
      this.user = null
      
      // Try to logout on server, but don't fail if it doesn't work
      axios.post(`${import.meta.env.VITE_API_BASE_URL}/logout`, {}, { 
        withCredentials: true 
      }).catch(() => {
        // Ignore logout errors
      })
      
      notifications.info('You have been logged out.')
    }
  },
})