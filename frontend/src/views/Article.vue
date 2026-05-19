<template>
  <article class="article-detail" v-if="article">
    <header class="article-header">
      <h1>{{ article.title }}</h1>
      <div class="article-meta">
        <span>{{ formatDate(article.created_at) }}</span>
        <span v-if="categoryName" class="meta-category">{{ categoryName }}</span>
        <span>{{ readTime }} 分钟阅读</span>
      </div>
    </header>
    <div class="paper">
      <div class="markdown-body">
        <MdPreview :modelValue="article.content" />
      </div>
    </div>
    <div class="article-footer">
      <router-link to="/" class="back-link">← 返回文章列表</router-link>
    </div>
  </article>
  <div class="loading" v-else-if="loading">加载中...</div>
  <div class="error" v-else>文章不存在</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle, getCategories } from '../api'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const route = useRoute()
const article = ref(null)
const loading = ref(true)
const categoryName = ref('')

const readTime = computed(() => {
  if (!article.value?.content) return 1
  return Math.max(1, Math.ceil(article.value.content.length / 500))
})

onMounted(() => fetchArticle())
watch(() => route.params.id, () => fetchArticle())

async function fetchArticle() {
  loading.value = true
  article.value = null
  try {
    const res = await getArticle(route.params.id)
    article.value = res.data
    if (article.value.category_id) {
      const catRes = await getCategories()
      const cat = catRes.data.find(c => c.id === article.value.category_id)
      categoryName.value = cat?.name || ''
    }
  } catch (e) {
    article.value = null
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<style scoped>
.article-detail { max-width: 780px; }

.article-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

.article-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--heading);
  line-height: 1.3;
  margin-bottom: 16px;
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: var(--text-secondary);
  flex-wrap: wrap;
}

.meta-category {
  background: var(--accent-bg);
  color: var(--accent);
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.paper {
  background: var(--paper-bg);
  border: 1px solid var(--paper-border);
  border-radius: 4px;
  padding: 40px 44px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.markdown-body {
  font-size: 17px;
  line-height: 2;
  color: var(--paper-text);
}

/* md-editor-v3 预览样式覆盖 */
.markdown-body :deep(.md-editor-preview) {
  background: transparent;
}

.markdown-body :deep(h2) {
  font-size: 24px;
  margin: 48px 0 20px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--paper-border);
  color: var(--paper-heading);
  font-weight: 600;
}

.markdown-body :deep(h3) {
  font-size: 20px;
  margin: 36px 0 14px;
  color: var(--paper-heading);
  font-weight: 600;
}

.markdown-body :deep(p) {
  margin-bottom: 20px;
  text-align: justify;
}

.markdown-body :deep(pre) {
  background: var(--paper-code-bg);
  padding: 18px 22px;
  border-radius: 4px;
  border: 1px solid var(--paper-border);
  overflow-x: auto;
  margin: 20px 0;
}

.markdown-body :deep(code) {
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
  color: var(--paper-text);
}

.markdown-body :deep(p code),
.markdown-body :deep(li code) {
  background: var(--paper-code-bg);
  padding: 2px 6px;
  border-radius: 3px;
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--paper-blockquote-border);
  background: var(--paper-blockquote-bg);
  padding: 14px 18px;
  color: var(--paper-secondary);
  margin: 20px 0;
  border-radius: 0 4px 4px 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin-bottom: 20px;
  padding-left: 28px;
}

.markdown-body :deep(li) {
  margin-bottom: 6px;
}

.markdown-body :deep(a) {
  color: var(--accent);
  border-bottom: 1px solid var(--accent);
}

.markdown-body :deep(a:hover) { opacity: 0.8; }

.markdown-body :deep(img) {
  border-radius: var(--radius);
  display: block;
  margin: 24px auto;
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid var(--paper-border);
  margin: 32px 0;
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--paper-border);
  padding: 10px 14px;
  text-align: left;
}

.markdown-body :deep(th) {
  background: var(--paper-code-bg);
  font-weight: 600;
}

.article-footer {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.back-link {
  font-size: 15px;
  color: var(--text-secondary);
  transition: color 0.15s;
}

.back-link:hover { color: var(--accent); }

@media (max-width: 767px) {
  .paper {
    padding: 24px 18px;
  }
  .article-header h1 { font-size: 24px; }
}

.loading, .error {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}
</style>
