<template>
  <div style="padding: 20px">
    <h1>Users</h1>
    <div>
      <input v-model="newUser.name" placeholder="Name" />
      <input v-model="newUser.email" placeholder="Email" />
      <button @click="addUser">Add User</button>
    </div>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.name }} ({{ user.email }})
        <button @click="deleteUser(user.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Interfaces
interface User {
  id: number
  name: string
  email: string
}

// API URL
const API_URL = 'http://localhost:8000'

// State
const users = ref<User[]>([])

const newUser = ref<{ name: string; email: string }>({ name: '', email: '' })

// Fetch users
const fetchUsers = async () => {
  const res = await axios.get<User[]>(`${API_URL}/users`)
  users.value = res.data
}

// Add user
const addUser = async () => {
  if (!newUser.value.name || !newUser.value.email) return
  await axios.post(`${API_URL}/users`, {
    name: newUser.value.name,
    email: newUser.value.email
  })
  newUser.value = { name: '', email: '' }
  fetchUsers()
}

// Delete user
const deleteUser = async (id: number) => {
  await axios.delete(`${API_URL}/users/${id}`)
  fetchUsers()
}

// On mount
onMounted(() => {
  fetchUsers()
})
</script>