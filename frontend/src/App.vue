<template>
  <nav>
    <router-link to="/users">Users</router-link> |
    <router-link to="/items">Items</router-link>
  </nav>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style scoped>
nav {
  padding: 1rem;
  background-color: #f0f0f0;
}
nav a {
  margin: 0 10px;
  text-decoration: none;
}
</style>