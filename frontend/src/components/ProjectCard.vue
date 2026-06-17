<template>
  <router-link :to="`/works/${project.id}`" class="project-card">
    <div class="card-image" v-if="project.image_url">
      <img :src="project.image_url" :alt="project.title" />
    </div>
    <div class="card-body">
      <h3 class="card-title">{{ project.title }}</h3>
      <p class="card-desc">{{ project.description }}</p>
      <div class="card-tags" v-if="tagList.length">
        <span class="tag" v-for="tag in tagList" :key="tag">{{ tag }}</span>
      </div>
      <div class="card-links">
        <a v-if="project.github_url" :href="project.github_url" target="_blank" @click.stop>GitHub</a>
        <a v-if="project.demo_url" :href="project.demo_url" target="_blank" @click.stop>在线演示</a>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  project: { type: Object, required: true },
})

const tagList = computed(() =>
  props.project.tags ? props.project.tags.split(',').map(t => t.trim()).filter(Boolean) : []
)
</script>

<style scoped>
.project-card {
  display: block;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: transform 0.15s, box-shadow 0.15s;
  text-decoration: none;
  color: inherit;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--card-hover-shadow);
}

.card-image {
  height: 180px;
  overflow: hidden;
  background: var(--bg-secondary);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 8px;
}

.card-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.tag {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 100px;
  background: var(--accent-bg);
  color: var(--accent);
}

.card-links {
  display: flex;
  gap: 16px;
}

.card-links a {
  font-size: 13px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.15s;
}

.card-links a:hover {
  color: var(--accent);
}
</style>
