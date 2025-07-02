import { defineStore } from 'pinia'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  timeout?: number
}

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    notifications: [] as Notification[]
  }),
  
  actions: {
    add(notification: Omit<Notification, 'id'>) {
      const id = Date.now().toString()
      const newNotification: Notification = {
        id,
        timeout: 5000,
        ...notification
      }
      
      this.notifications.push(newNotification)
      
      // Auto-remove after timeout
      if (newNotification.timeout) {
        setTimeout(() => {
          this.remove(id)
        }, newNotification.timeout)
      }
      
      return id
    },
    
    success(message: string, timeout?: number) {
      return this.add({ type: 'success', message, timeout })
    },
    
    error(message: string, timeout?: number) {
      return this.add({ type: 'error', message, timeout })
    },
    
    warning(message: string, timeout?: number) {
      return this.add({ type: 'warning', message, timeout })
    },
    
    info(message: string, timeout?: number) {
      return this.add({ type: 'info', message, timeout })
    },
    
    remove(id: string) {
      const index = this.notifications.findIndex(n => n.id === id)
      if (index > -1) {
        this.notifications.splice(index, 1)
      }
    },
    
    clear() {
      this.notifications = []
    }
  }
}) 