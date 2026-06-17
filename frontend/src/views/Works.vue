<template>
  <div class="works">
    <h1>作品</h1>

    <div class="tags-bar" v-if="allTags.length">
      <button
        :class="{ active: activeTag === null }"
        @click="filterBy(null)"
      >全部</button>
      <button
        v-for="tag in allTags"
        :key="tag"
        :class="{ active: activeTag === tag }"
        @click="filterBy(tag)"
      >{{ tag }}</button>
    </div>

    <div class="project-grid" v-if="filteredProjects.length">
      <ProjectCard v-for="p in filteredProjects" :key="p.id" :project="p" />
    </div>
    <div class="empty" v-else>
      <p>暂无作品</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getProjects } from '../api'
import ProjectCard from '../components/ProjectCard.vue'

const projects = ref([])
const activeTag = ref(null)

const allTags = computed(() => {
  const tags = new Set()
  projects.value.forEach(p => {
    if (p.tags) p.tags.split(',').map(t => t.trim()).filter(Boolean).forEach(t => tags.add(t))
  })
  return [...tags]
})

const filteredProjects = computed(() => {
  if (!activeTag.value) return projects.value
  return projects.value.filter(p =>
    p.tags && p.tags.split(',').map(t => t.trim()).includes(activeTag.value)
  )
})

function filterBy(tag) {
  activeTag.value = tag
}

onMounted(async () => {
  try {
    const res = await getProjects({ limit: 100 })
    projects.value = res.data
  } catch (e) { /* ignore */ }
})
</script>

<style scoped>
.works { max-width: 1200px; margin: 0 auto; }

h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--heading);
  margin-bottom: 32px;
}

.tags-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 36px;
}

.tags-bar button {
  padding: 6px 16px;
  border: 1px solid var(--border);
  border-radius: 100px;
  background: var(--bg);
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}

.tags-bar button:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.tags-bar button.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

@media (max-width: 767px) {
  .project-grid { grid-template-columns: 1fr; }
}
</style>
