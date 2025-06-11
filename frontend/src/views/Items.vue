<template>
  <div style="padding: 20px">

    <h1>Items</h1>
    <div>
      <input v-model="newItem.name" placeholder="Name" />
      <input v-model="newItem.description" placeholder="Description" />
      <input v-model.number="newItem.price" placeholder="Price" />
      <button @click="addItem">Add Item</button>
    </div>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} - {{ item.description }} - {{ item.price }}
        <button @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Item {
  id: number
  name: string
  description: string
  price: number
}

// API URL
const API_URL = import.meta.env.VITE_API_BASE_URL;

// State
const items = ref<Item[]>([])

const newItem = ref<{ name: string; description: string; price: number }>({ name: '', description: '', price: 0 })

// Fetch items
const fetchItems = async () => {
  const res = await axios.get<Item[]>(`${API_URL}/items`)
  items.value = res.data
}

// Add item
const addItem = async () => {
  if (!newItem.value.name || !newItem.value.description || newItem.value.price === null) return
  await axios.post(`${API_URL}/items`, {
    name: newItem.value.name,
    description: newItem.value.description,
    price: newItem.value.price 
  })
  newItem.value = { name: '', description: '', price: 0 }
  fetchItems()
}

// Delete item
const deleteItem = async (id: number) => {
  await axios.delete(`${API_URL}/items/${id}`)
  fetchItems()
}

// On mount
onMounted(() => {
  fetchItems()
})
</script>