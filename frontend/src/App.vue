<template>
  <div class="layout">
    <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">☰</button>
    <Sidebar
      :is-open="sidebarOpen"
      @close="sidebarOpen = false"
      @select-category="sidebarOpen = false"
    />
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'
const sidebarOpen = ref(false)
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}
.main {
  flex: 1;
  padding: 40px 48px;
  max-width: 100%;
  min-width: 0;
}
.menu-btn {
  display: none;
  position: fixed;
  top: 12px;
  left: 12px;
  z-index: 100;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 8px 12px;
  font-size: 20px;
  cursor: pointer;
  color: var(--text);
}
@media (max-width: 767px) {
  .menu-btn { display: block; }
  .main { padding: 56px 16px 24px; }
}
</style>
