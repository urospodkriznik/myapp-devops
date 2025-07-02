<template>
  <v-app>
    <v-app-bar app elevation="1">
      <v-app-bar-nav-icon @click="drawer = !drawer" class="d-md-none" />
      
      <v-toolbar-title class="d-flex align-center">
        <v-icon icon="mdi-cube-outline" class="mr-2" />
        MyApp
      </v-toolbar-title>
      
      <v-spacer />
      
      <!-- Desktop Navigation -->
      <div class="d-none d-md-flex">
        <v-btn 
          text 
          to="/items" 
          v-if="auth.user"
          prepend-icon="mdi-package-variant"
        >
          Items
        </v-btn>
        <v-btn 
          text 
          to="/users" 
          v-if="auth.user"
          prepend-icon="mdi-account-group"
        >
          Users
        </v-btn>
        <v-btn 
          text 
          to="/login" 
          v-if="!auth.user"
          prepend-icon="mdi-login"
        >
          Login
        </v-btn>
        <v-btn 
          text 
          to="/register" 
          v-if="!auth.user"
          prepend-icon="mdi-account-plus"
        >
          Register
        </v-btn>
      </div>
      
      <!-- User Menu -->
      <v-menu v-if="auth.user" offset-y>
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            variant="text"
            class="ml-2"
          >
            <v-avatar size="32" class="mr-2">
              <v-icon icon="mdi-account" />
            </v-avatar>
            {{ auth.user.name }}
            <v-icon icon="mdi-chevron-down" class="ml-1" />
          </v-btn>
        </template>
        
        <v-list>
          <v-list-item @click="showProfile">
            <template v-slot:prepend>
              <v-icon icon="mdi-account" />
            </template>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>
          
          <v-divider />
          
          <v-list-item @click="logout">
            <template v-slot:prepend>
              <v-icon icon="mdi-logout" />
            </template>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Mobile Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list>
        <v-list-item>
          <template v-slot:prepend>
            <v-icon icon="mdi-cube-outline" />
          </template>
          <v-list-item-title>MyApp</v-list-item-title>
        </v-list-item>
        
        <v-divider />
        
        <v-list-item 
          to="/items" 
          v-if="auth.user"
          prepend-icon="mdi-package-variant"
        >
          <v-list-item-title>Items</v-list-item-title>
        </v-list-item>
        
        <v-list-item 
          to="/users" 
          v-if="auth.user"
          prepend-icon="mdi-account-group"
        >
          <v-list-item-title>Users</v-list-item-title>
        </v-list-item>
        
        <v-list-item 
          to="/login" 
          v-if="!auth.user"
          prepend-icon="mdi-login"
        >
          <v-list-item-title>Login</v-list-item-title>
        </v-list-item>
        
        <v-list-item 
          to="/register" 
          v-if="!auth.user"
          prepend-icon="mdi-account-plus"
        >
          <v-list-item-title>Register</v-list-item-title>
        </v-list-item>
        
        <v-divider v-if="auth.user" />
        
        <v-list-item 
          @click="logout" 
          v-if="auth.user"
          prepend-icon="mdi-logout"
        >
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

    <!-- Notification System -->
    <NotificationSystem />
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notifications'
import NotificationSystem from '@/components/NotificationSystem.vue'

const auth = useAuthStore()
const router = useRouter()
const notifications = useNotificationStore()
const drawer = ref(false)

const logout = () => {
  auth.logout()
  router.push('/login')
}

const showProfile = () => {
  notifications.info('Profile feature coming soon!')
}
</script>