<template>
  <aside class="sidebar" :class="{ open: isOpen }">
    <div class="sidebar-header">
      <router-link to="/" class="logo" @click="close">个人博客</router-link>
    </div>

    <div class="search-box">
      <input
        v-model="query"
        type="text"
        placeholder="搜索文章..."
        @keyup.enter="search"
      />
    </div>

    <nav class="category-nav">
      <h3>分类</h3>
      <ul>
        <li>
          <router-link
            to="/"
            :class="{ active: !activeCategory }"
            @click="handleCategory(null)"
          >
            全部
          </router-link>
        </li>
        <li v-for="cat in categories" :key="cat.id">
          <router-link
            :to="`/?category=${cat.id}`"
            :class="{ active: activeCategory === cat.id }"
            @click="handleCategory(cat.id)"
          >
            {{ cat.name }}
          </router-link>
        </li>
      </ul>
    </nav>

    <div class="sidebar-footer">
      <button class="theme-toggle" @click="toggleTheme" :title="themeLabel">
        {{ themeIcon }}
      </button>
      <router-link to="/about" class="about-link" @click="close">关于</router-link>
    </div>
  </aside>
  <div class="overlay" v-if="isOpen" @click="close"></div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCategories } from '../api'

const props = defineProps({
  isOpen: Boolean,
})
const emit = defineEmits(['close', 'select-category'])

const route = useRoute()
const router = useRouter()
const categories = ref([])
const query = ref(route.query.q || '')

const activeCategory = computed(() => {
  const cat = route.query.category
  return cat ? Number(cat) : null
})

const themeIcon = ref('🌙')
const themeLabel = computed(() =>
  document.documentElement.dataset.theme === 'dark' ? '切换亮色' : '切换暗色'
)

onMounted(async () => {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch (e) {
    console.error('加载分类失败', e)
  }
  initTheme()
})

function initTheme() {
  const saved = localStorage.getItem('theme')
  if (saved) {
    document.documentElement.dataset.theme = saved
  } else {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    document.documentElement.dataset.theme = prefersDark ? 'dark' : 'light'
  }
  themeIcon.value = document.documentElement.dataset.theme === 'dark' ? '☀️' : '🌙'
}

function toggleTheme() {
  const current = document.documentElement.dataset.theme
  const next = current === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = next
  localStorage.setItem('theme', next)
  themeIcon.value = next === 'dark' ? '☀️' : '🌙'
}

function search() {
  const params = { ...route.query, q: query.value || undefined, page: undefined }
  if (!query.value) delete params.q
  router.push({ path: '/', query: params })
}

function handleCategory(id) {
  emit('select-category', id)
  close()
}

function close() {
  emit('close')
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  min-width: 260px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 24px 20px;
  height: 100vh;
  position: sticky;
  top: 0;
  overflow-y: auto;
}

.sidebar-header { margin-bottom: 24px; }

.logo {
  font-size: 22px;
  font-weight: 700;
  color: var(--heading);
}

.search-box {
  margin-bottom: 24px;
}

.search-box input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.search-box input:focus { border-color: var(--accent); }

.category-nav { flex: 1; }
.category-nav h3 {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  margin-bottom: 12px;
}
.category-nav ul { list-style: none; }
.category-nav li { margin-bottom: 4px; }
.category-nav a {
  display: block;
  padding: 6px 12px;
  border-radius: var(--radius);
  color: var(--text-secondary);
  font-size: 14px;
  transition: background 0.15s, color 0.15s;
}
.category-nav a:hover,
.category-nav a.active {
  background: var(--accent-bg);
  color: var(--accent);
}

.sidebar-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}

.theme-toggle {
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 6px 10px;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}

.about-link {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 手机汉堡按钮 */
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
}

.overlay { display: none; }

@media (max-width: 767px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 200;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
  }
  .sidebar.open { transform: translateX(0); }
  .overlay {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 199;
    background: rgba(0, 0, 0, 0.4);
  }
}
</style>
