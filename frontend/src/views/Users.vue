<template>
  <v-container>
    <v-card class="pa-6" elevation="2">
      <v-card-title class="d-flex align-center">
        <v-icon icon="mdi-account-group" class="mr-2" />
        User Management
        <v-spacer />
        <v-chip color="primary" variant="outlined">
          {{ users.length }} users
        </v-chip>
      </v-card-title>

      <v-form @submit.prevent="addUser" class="mb-6">
        <v-row dense>
          <v-col cols="12" sm="3">
            <v-text-field 
              v-model="newUser.name" 
              label="Name" 
              variant="outlined" 
              dense 
              required 
              :disabled="loading"
              prepend-inner-icon="mdi-account"
            />
          </v-col>
          <v-col cols="12" sm="3">
            <v-text-field 
              v-model="newUser.email" 
              label="Email" 
              type="email"
              variant="outlined" 
              dense 
              required 
              :disabled="loading"
              prepend-inner-icon="mdi-email"
            />
          </v-col>
          <v-col cols="12" sm="3">
            <v-text-field 
              v-model="newUser.password" 
              label="Password" 
              type="password" 
              variant="outlined" 
              dense 
              required 
              :disabled="loading"
              prepend-inner-icon="mdi-lock"
            />
          </v-col>
          <v-col cols="12" sm="2" class="d-flex align-center">
            <v-btn 
              type="submit" 
              color="primary" 
              :loading="loading"
              :disabled="!isFormValid || loading"
              block
            >
              <v-icon icon="mdi-plus" class="mr-1" />
              Add
            </v-btn>
          </v-col>
        </v-row>
      </v-form>

      <v-divider class="mb-4" />

      <div v-if="loading && users.length === 0" class="text-center py-8">
        <v-progress-circular indeterminate color="primary" />
        <p class="mt-2 text-medium-emphasis">Loading users...</p>
      </div>

      <div v-else-if="users.length === 0" class="text-center py-8">
        <v-icon icon="mdi-account-group-outline" size="64" color="grey" />
        <p class="mt-2 text-medium-emphasis">No users found</p>
        <p class="text-caption">Add your first user using the form above</p>
      </div>

      <v-list v-else>
        <v-list-item
          v-for="user in users"
          :key="user.id"
          class="mb-2"
          elevation="1"
          rounded
        >
          <template v-slot:prepend>
            <v-avatar color="primary" size="40">
              <v-icon icon="mdi-account" color="white" />
            </v-avatar>
          </template>

          <v-list-item-title class="font-weight-medium">
            {{ user.name }}
          </v-list-item-title>
          
          <v-list-item-subtitle>
            {{ user.email }}
          </v-list-item-subtitle>

          <template v-slot:append>
            <v-btn 
              icon 
              color="error" 
              variant="text"
              @click="confirmDelete(user)"
              :disabled="loading"
            >
              <v-icon icon="mdi-delete" />
            </v-btn>
          </template>
        </v-list-item>
      </v-list>
    </v-card>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          <v-icon icon="mdi-delete" color="error" class="mr-2" />
          Delete User
        </v-card-title>
        
        <v-card-text>
          Are you sure you want to delete user "<strong>{{ userToDelete?.name }}</strong>"?
          This action cannot be undone.
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn 
            color="error" 
            @click="deleteUserConfirmed"
            :loading="loading"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useNotificationStore } from '@/stores/notifications'

interface User {
  id: number
  name: string
  email: string
}

const API = import.meta.env.VITE_API_BASE_URL
const notifications = useNotificationStore()

const users = ref<User[]>([])
const newUser = ref({ name: '', email: '', password: '' })
const loading = ref(false)
const deleteDialog = ref(false)
const userToDelete = ref<User | null>(null)

const isFormValid = computed(() => {
  return newUser.value.name.trim() && 
         newUser.value.email.trim() && 
         newUser.value.password.trim().length >= 6
})

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API}/users`)
    users.value = res.data
  } catch (error: any) {
    console.error('Error fetching users:', error)
    if (error.response?.status === 401) {
      notifications.error('Please log in to view users.')
    } else if (error.response?.status === 403) {
      notifications.error('You do not have permission to view users.')
    } else {
      notifications.error('Failed to load users. Please try again.')
    }
  } finally {
    loading.value = false
  }
}

const addUser = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  try {
    await axios.post(`${API}/register`, newUser.value)
    newUser.value = { name: '', email: '', password: '' }
    await fetchUsers()
    notifications.success('User added successfully!')
  } catch (error: any) {
    console.error('Error adding user:', error)
    if (error.response?.status === 400) {
      const detail = error.response.data?.detail
      if (typeof detail === 'string') {
        notifications.error(detail)
      } else {
        notifications.error('Failed to add user. Please check your input.')
      }
    } else {
      notifications.error('Failed to add user. Please try again.')
    }
  } finally {
    loading.value = false
  }
}

const confirmDelete = (user: User) => {
  userToDelete.value = user
  deleteDialog.value = true
}

const deleteUserConfirmed = async () => {
  if (!userToDelete.value) return
  
  loading.value = true
  try {
    await axios.delete(`${API}/users/${userToDelete.value.id}`)
    await fetchUsers()
    notifications.success('User deleted successfully!')
  } catch (error: any) {
    console.error('Error deleting user:', error)
    if (error.response?.status === 401) {
      notifications.error('Please log in to delete users.')
    } else if (error.response?.status === 403) {
      notifications.error('You do not have permission to delete users.')
    } else if (error.response?.status === 404) {
      notifications.error('User not found.')
    } else {
      notifications.error('Failed to delete user. Please try again.')
    }
  } finally {
    loading.value = false
    deleteDialog.value = false
    userToDelete.value = null
  }
}

onMounted(fetchUsers)
</script>