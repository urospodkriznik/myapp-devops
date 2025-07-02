<template>
  <v-container>
    <v-card class="pa-6" elevation="2">
      <v-card-title class="d-flex align-center">
        <v-icon icon="mdi-package-variant" class="mr-2" />
        Items Management
        <v-spacer />
        <v-chip color="primary" variant="outlined">
          {{ items.length }} items
        </v-chip>
      </v-card-title>

      <v-form @submit.prevent="addItem" class="mb-6">
        <v-row dense>
          <v-col cols="12" sm="4">
            <v-text-field 
              v-model="newItem.name" 
              label="Name" 
              variant="outlined" 
              dense 
              required 
              :disabled="loading"
              prepend-inner-icon="mdi-tag"
            />
          </v-col>
          <v-col cols="12" sm="4">
            <v-text-field 
              v-model="newItem.description" 
              label="Description" 
              variant="outlined" 
              dense 
              required 
              :disabled="loading"
              prepend-inner-icon="mdi-text"
            />
          </v-col>
          <v-col cols="12" sm="3">
            <v-text-field 
              v-model.number="newItem.price" 
              label="Price" 
              type="number" 
              variant="outlined" 
              dense 
              required 
              :disabled="loading"
              prepend-inner-icon="mdi-currency-usd"
              min="0"
              step="0.01"
            />
          </v-col>
          <v-col cols="12" sm="1" class="d-flex align-center">
            <v-btn 
              type="submit" 
              color="primary" 
              :loading="loading"
              :disabled="!isFormValid || loading"
              icon
            >
              <v-icon icon="mdi-plus" />
            </v-btn>
          </v-col>
        </v-row>
      </v-form>

      <v-divider class="mb-4" />

      <div v-if="loading && items.length === 0" class="text-center py-8">
        <v-progress-circular indeterminate color="primary" />
        <p class="mt-2 text-medium-emphasis">Loading items...</p>
      </div>

      <div v-else-if="items.length === 0" class="text-center py-8">
        <v-icon icon="mdi-package-variant-closed" size="64" color="grey" />
        <p class="mt-2 text-medium-emphasis">No items found</p>
        <p class="text-caption">Add your first item using the form above</p>
      </div>

      <v-list v-else>
        <v-list-item
          v-for="item in items"
          :key="item.id"
          class="mb-2"
          elevation="1"
          rounded
        >
          <template v-slot:prepend>
            <v-avatar color="primary" size="40">
              <v-icon icon="mdi-package-variant" color="white" />
            </v-avatar>
          </template>

          <v-list-item-title class="font-weight-medium">
            {{ item.name }}
          </v-list-item-title>
          
          <v-list-item-subtitle>
            {{ item.description }}
          </v-list-item-subtitle>

          <template v-slot:append>
            <div class="d-flex align-center">
              <v-chip color="success" variant="outlined" class="mr-2">
                ${{ item.price.toFixed(2) }}
              </v-chip>
              
              <v-btn 
                icon 
                color="error" 
                variant="text"
                @click="confirmDelete(item)"
                :disabled="loading"
              >
                <v-icon icon="mdi-delete" />
              </v-btn>
            </div>
          </template>
        </v-list-item>
      </v-list>
    </v-card>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          <v-icon icon="mdi-delete" color="error" class="mr-2" />
          Delete Item
        </v-card-title>
        
        <v-card-text>
          Are you sure you want to delete "<strong>{{ itemToDelete?.name }}</strong>"?
          This action cannot be undone.
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn 
            color="error" 
            @click="deleteItemConfirmed"
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

interface Item {
  id: number
  name: string
  description: string
  price: number
}

const API = import.meta.env.VITE_API_BASE_URL
const notifications = useNotificationStore()

const items = ref<Item[]>([])
const newItem = ref({ name: '', description: '', price: 0 })
const loading = ref(false)
const deleteDialog = ref(false)
const itemToDelete = ref<Item | null>(null)

const isFormValid = computed(() => {
  return newItem.value.name.trim() && 
         newItem.value.description.trim() && 
         newItem.value.price > 0
})

const fetchItems = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API}/items`)
    items.value = res.data
  } catch (error: any) {
    console.error('Error fetching items:', error)
    notifications.error('Failed to load items. Please try again.')
  } finally {
    loading.value = false
  }
}

const addItem = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  try {
    await axios.post(`${API}/items`, newItem.value)
    newItem.value = { name: '', description: '', price: 0 }
    await fetchItems()
    notifications.success('Item added successfully!')
  } catch (error: any) {
    console.error('Error adding item:', error)
    if (error.response?.status === 401) {
      notifications.error('Please log in to add items.')
    } else {
      notifications.error('Failed to add item. Please try again.')
    }
  } finally {
    loading.value = false
  }
}

const confirmDelete = (item: Item) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const deleteItemConfirmed = async () => {
  if (!itemToDelete.value) return
  
  loading.value = true
  try {
    await axios.delete(`${API}/items/${itemToDelete.value.id}`)
    await fetchItems()
    notifications.success('Item deleted successfully!')
  } catch (error: any) {
    console.error('Error deleting item:', error)
    if (error.response?.status === 401) {
      notifications.error('Please log in to delete items.')
    } else if (error.response?.status === 404) {
      notifications.error('Item not found.')
    } else {
      notifications.error('Failed to delete item. Please try again.')
    }
  } finally {
    loading.value = false
    deleteDialog.value = false
    itemToDelete.value = null
  }
}

onMounted(fetchItems)
</script>