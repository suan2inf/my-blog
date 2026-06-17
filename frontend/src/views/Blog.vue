<template>
  <div class="blog">
    <div class="blog-head">
      <h1>博客</h1>
      <div class="search-box">
        <input
          v-model="query"
          type="text"
          placeholder="搜索文章..."
          @keyup.enter="search"
        />
      </div>
    </div>

    <div class="category-bar" v-if="categories.length">
      <button
        :class="{ active: activeCategory === null }"
        @click="filterCategory(null)"
      >全部</button>
      <button
        v-for="cat in categories"
        :key="cat.id"
        :class="{ active: activeCategory === cat.id }"
        @click="filterCategory(cat.id)"
      >{{ cat.name }}</button>
    </div>

    <div class="section-header" v-if="searchQuery">
      搜索: "{{ searchQuery }}"
    </div>

    <div class="article-grid" v-if="articles.length">
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
        :category-name="categoryMap[article.category_id]"
      />
    </div>
    <div class="empty" v-else-if="!loading">
      <p>暂无文章</p>
    </div>

    <Pagination
      :current-page="currentPage"
      :total-pages="totalPages"
      @change="goToPage"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticles, getCategories } from '../api'
import ArticleCard from '../components/ArticleCard.vue'
import Pagination from '../components/Pagination.vue'

const route = useRoute()
const router = useRouter()
const articles = ref([])
const loading = ref(false)
const categories = ref([])
const categoryMap = ref({})
const totalPages = ref(1)
const query = ref('')

const PAGE_SIZE = 9

const currentPage = computed(() => Number(route.query.page) || 1)
const activeCategory = computed(() => route.query.category ? Number(route.query.category) : null)
const searchQuery = computed(() => route.query.q || '')

onMounted(async () => {
  try {
    const res = await getCategories()
    categories.value = res.data
    res.data.forEach(c => { categoryMap.value[c.id] = c.name })
  } catch (e) { /* ignore */ }
  fetchArticles()
})

watch([() => route.query.page, () => route.query.q, () => route.query.category], () => {
  fetchArticles()
})

async function fetchArticles() {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * PAGE_SIZE,
      limit: PAGE_SIZE,
    }
    if (activeCategory.value) params.category_id = activeCategory.value
    if (searchQuery.value) params.q = searchQuery.value

    const res = await getArticles(params)
    articles.value = res.data
    totalPages.value = res.data.length < PAGE_SIZE ? currentPage.value : currentPage.value + 1
  } catch (e) {
    articles.value = []
  } finally {
    loading.value = false
  }
}

function goToPage(page) {
  const query = { ...route.query, page: page > 1 ? page : undefined }
  if (page <= 1) delete query.page
  router.push({ path: '/blog', query })
}

function search() {
  const params = { ...route.query, q: query.value || undefined, page: undefined }
  if (!query.value) delete params.q
  router.push({ path: '/blog', query: params })
}

function filterCategory(id) {
  const params = { ...route.query, category: id || undefined, page: undefined }
  if (!id) delete params.category
  router.push({ path: '/blog', query: params })
}

function navigate(path) {
  router.push(path)
}
</script>

<style scoped>
.blog { max-width: 1200px; margin: 0 auto; }

.blog-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 16px;
}

.blog-head h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--heading);
}

.search-box input {
  padding: 8px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  outline: none;
  width: 240px;
  transition: border-color 0.2s;
}

.search-box input:focus { border-color: var(--accent); }

.category-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 32px;
}

.category-bar button {
  padding: 6px 16px;
  border: 1px solid var(--border);
  border-radius: 100px;
  background: var(--bg);
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}

.category-bar button:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.category-bar button.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.section-header {
  font-size: 15px;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

@media (max-width: 767px) {
  .article-grid { grid-template-columns: 1fr; }
  .search-box input { width: 100%; }
}
</style>
