<template>
  <div class="work-detail" v-if="project">
    <router-link to="/works" class="back-link">← 返回作品列表</router-link>

    <header class="work-header">
      <div class="work-image" v-if="project.image_url">
        <img :src="project.image_url" :alt="project.title" />
      </div>
      <h1>{{ project.title }}</h1>
      <p class="work-desc">{{ project.description }}</p>
      <div class="work-meta">
        <div class="work-tags" v-if="tagList.length">
          <span class="tag" v-for="tag in tagList" :key="tag">{{ tag }}</span>
        </div>
        <div class="work-links">
          <a v-if="project.github_url" :href="project.github_url" target="_blank" class="link-btn">GitHub</a>
          <a v-if="project.demo_url" :href="project.demo_url" target="_blank" class="link-btn demo">在线演示</a>
        </div>
      </div>
    </header>

    <article class="work-content paper" v-if="project.content">
      <MdPreview :model-value="project.content" />
    </article>
  </div>

  <div class="not-found" v-else-if="!loading">
    <h2>作品不存在</h2>
    <router-link to="/works">返回作品列表</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProject } from '../api'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const route = useRoute()
const project = ref(null)
const loading = ref(true)

const tagList = computed(() =>
  project.value?.tags ? project.value.tags.split(',').map(t => t.trim()).filter(Boolean) : []
)

onMounted(async () => {
  try {
    const res = await getProject(route.params.id)
    project.value = res.data
  } catch (e) {
    project.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.work-detail { max-width: 800px; margin: 0 auto; }

.back-link {
  display: inline-block;
  margin-bottom: 32px;
  font-size: 14px;
  color: var(--text-secondary);
  text-decoration: none;
}

.back-link:hover { color: var(--accent); }

.work-header {
  margin-bottom: 40px;
}

.work-image {
  margin-bottom: 24px;
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg-secondary);
}

.work-image img {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  display: block;
}

.work-header h1 {
  font-size: 32px;
  font-weight: 800;
  color: var(--heading);
  margin-bottom: 12px;
}

.work-desc {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 20px;
  line-height: 1.7;
}

.work-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.work-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 100px;
  background: var(--accent-bg);
  color: var(--accent);
}

.work-links {
  display: flex;
  gap: 10px;
}

.link-btn {
  padding: 6px 18px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 14px;
  text-decoration: none;
  color: var(--text);
  transition: all 0.15s;
}

.link-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.link-btn.demo {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.link-btn.demo:hover {
  background: var(--accent-hover);
}

/* 文章阅读区 */
.work-content {
  border-top: 1px solid var(--border);
  padding-top: 32px;
}

.paper {
  background: var(--paper-bg);
  border: 1px solid var(--paper-border);
  border-radius: var(--radius);
  padding: 40px 48px;
  color: var(--paper-text);
  line-height: 1.85;
}

.paper :deep(h2) { font-size: 24px; margin: 32px 0 16px; color: var(--paper-heading); }
.paper :deep(h3) { font-size: 18px; margin: 24px 0 12px; color: var(--paper-heading); }
.paper :deep(p) { margin-bottom: 16px; }
.paper :deep(pre) { background: var(--paper-code-bg); border-radius: var(--radius); padding: 16px 20px; overflow-x: auto; margin-bottom: 16px; }
.paper :deep(blockquote) { border-left: 3px solid var(--paper-blockquote-border); background: var(--paper-blockquote-bg); padding: 12px 16px; margin-bottom: 16px; color: var(--paper-secondary); }
.paper :deep(a) { color: var(--accent); }
.paper :deep(code) { background: var(--paper-code-bg); padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
.paper :deep(pre code) { background: none; padding: 0; }
.paper :deep(img) { border-radius: var(--radius); }
.paper :deep(table) { width: 100%; border-collapse: collapse; margin-bottom: 16px; }
.paper :deep(th), .paper :deep(td) { border: 1px solid var(--paper-border); padding: 8px 12px; text-align: left; }

.not-found {
  text-align: center;
  padding: 80px 20px;
}

.not-found h2 {
  font-size: 20px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

@media (max-width: 767px) {
  .work-header h1 { font-size: 24px; }
  .paper { padding: 24px 20px; }
}
</style>
