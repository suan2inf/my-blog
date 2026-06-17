<template>
  <div class="landing">
    <!-- Hero -->
    <section class="hero">
      <h1 class="hero-title">算不尽的博客网站</h1>
      <p class="hero-subtitle">我叫算不尽，这是我的个人博客网站，主做作品展示与经验分享，欢迎观看</p>
    </section>

    <!-- 精选作品 -->
    <section class="section" v-if="projects.length">
      <div class="section-head">
        <h2>精选作品</h2>
        <router-link to="/works" class="more-link">查看全部 →</router-link>
      </div>
      <div class="project-grid">
        <ProjectCard v-for="p in projects" :key="p.id" :project="p" />
      </div>
    </section>

    <!-- 最新文章 -->
    <section class="section">
      <div class="section-head">
        <h2>最新文章</h2>
        <router-link to="/blog" class="more-link">查看全部 →</router-link>
      </div>
      <div class="article-grid" v-if="articles.length">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
          :category-name="categoryMap[article.category_id]"
        />
      </div>
      <div class="empty" v-else>
        <p>暂无文章</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProjects, getArticles, getCategories } from '../api'
import ProjectCard from '../components/ProjectCard.vue'
import ArticleCard from '../components/ArticleCard.vue'

const projects = ref([])
const articles = ref([])
const categoryMap = ref({})

onMounted(async () => {
  try {
    const [pRes, aRes, cRes] = await Promise.all([
      getProjects({ featured: true, limit: 6 }),
      getArticles({ limit: 6 }),
      getCategories(),
    ])
    projects.value = pRes.data
    articles.value = aRes.data
    cRes.data.forEach(c => { categoryMap.value[c.id] = c.name })
  } catch (e) { /* ignore */ }
})
</script>

<style scoped>
/* Hero */
.hero {
  padding: 80px 0 64px;
  text-align: center;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  color: var(--heading);
  letter-spacing: -1px;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 20px;
  color: var(--accent);
  margin-bottom: 24px;
}

.hero-bio {
  font-size: 16px;
  color: var(--text-secondary);
  max-width: 560px;
  margin: 0 auto;
  line-height: 1.8;
}

/* Section */
.section {
  margin-bottom: 72px;
}

.section-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.section-head h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--heading);
}

.more-link {
  font-size: 14px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.15s;
}

.more-link:hover { color: var(--accent); }

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

@media (max-width: 767px) {
  .hero { padding: 48px 0 40px; }
  .hero-title { font-size: 32px; }
  .hero-subtitle { font-size: 17px; }
  .hero-bio { font-size: 15px; }
  .project-grid { grid-template-columns: 1fr; }
  .article-grid { grid-template-columns: 1fr; }
}
</style>
