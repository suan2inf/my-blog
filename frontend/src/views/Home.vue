<template>
  <div class="home">
    <!-- Hero 区 -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">DSM 的博客</h1>
        <p class="hero-subtitle">记录学习、思考与构建的过程</p>
        <div class="hero-stats" v-if="stats.articles > 0">
          <div class="stat">
            <span class="stat-num">{{ stats.articles }}</span>
            <span class="stat-label">篇文章</span>
          </div>
          <div class="stat">
            <span class="stat-num">{{ stats.categories }}</span>
            <span class="stat-label">个分类</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 文章列表区 -->
    <section class="articles-section">
      <div class="section-header">
        <h2 v-if="searchQuery">搜索: "{{ searchQuery }}"</h2>
        <h2 v-else-if="activeCategory && categoryMap[activeCategory]">{{ categoryMap[activeCategory] }}</h2>
        <h2 v-else>最新文章</h2>
      </div>

      <div class="card-grid" v-if="articles.length">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
          :category-name="categoryMap[article.category_id]"
        />
      </div>
      <div class="empty" v-else-if="!loading">
        <p>暂无文章</p>
        <p class="empty-hint">在后台创建文章后会自动显示在这里</p>
      </div>

      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        @change="goToPage"
      />
    </section>
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
const totalPages = ref(1)
const categoryMap = ref({})

const currentPage = computed(() => Number(route.query.page) || 1)
const activeCategory = computed(() => route.query.category ? Number(route.query.category) : null)
const searchQuery = computed(() => route.query.q || '')

const stats = ref({ articles: 0, categories: 0 })

const PAGE_SIZE = 9

onMounted(async () => {
  try {
    const catRes = await getCategories()
    catRes.data.forEach(c => { categoryMap.value[c.id] = c.name })
    stats.value.categories = catRes.data.length
  } catch (e) { /* ignore */ }
  try {
    const res = await getArticles({ limit: 1000 })
    stats.value.articles = res.data.length
  } catch (e) { /* ignore */ }
  fetchArticles()
})

watch([() => route.query.page, () => route.query.q, () => route.query.category], () => {
  fetchArticles()
})

async function fetchStats() {
  try {
    const res = await getArticles({ limit: 1 })
    allArticlesCount = res.data.length
  } catch (e) { /* ignore */ }
}

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
  router.push({ path: '/', query })
}
</script>

<style scoped>
/* ===== Hero ===== */
.hero {
  margin-bottom: 56px;
  padding: 48px 0 32px;
}

.hero-content { max-width: 600px; }

.hero-title {
  font-size: 40px;
  font-weight: 800;
  color: var(--heading);
  letter-spacing: -0.5px;
  margin-bottom: 12px;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  margin-bottom: 28px;
}

.hero-stats {
  display: flex;
  gap: 32px;
}

.stat {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.stat-num {
  font-size: 32px;
  font-weight: 700;
  color: var(--accent);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

/* ===== 文章区 ===== */
.articles-section {
  border-top: 1px solid var(--border);
  padding-top: 32px;
}

.section-header {
  margin-bottom: 28px;
}

.section-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-secondary);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

.empty-hint {
  font-size: 14px;
  margin-top: 8px;
  opacity: 0.7;
}

@media (max-width: 767px) {
  .hero {
    padding: 24px 0 24px;
    margin-bottom: 32px;
  }
  .hero-title { font-size: 28px; }
  .hero-subtitle { font-size: 16px; }
  .stat-num { font-size: 24px; }
  .card-grid { grid-template-columns: 1fr; }
}
</style>
