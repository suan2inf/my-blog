<template>
  <div class="pagination" v-if="totalPages > 1">
    <button :disabled="currentPage <= 1" @click="$emit('change', currentPage - 1)">
      ‹
    </button>
    <button
      v-for="page in pages"
      :key="page"
      :class="{ active: page === currentPage }"
      :disabled="page === '...'"
      @click="page !== '...' && $emit('change', page)"
    >
      {{ page }}
    </button>
    <button :disabled="currentPage >= totalPages" @click="$emit('change', currentPage + 1)">
      ›
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages: { type: Number, required: true },
})
defineEmits(['change'])

const pages = computed(() => {
  const p = []
  const total = props.totalPages
  const cur = props.currentPage
  const range = 2

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= cur - range && i <= cur + range)) {
      p.push(i)
    } else if (p[p.length - 1] !== '...') {
      p.push('...')
    }
  }
  return p
})
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 32px 0;
}

.pagination button {
  min-width: 36px;
  height: 36px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg);
  color: var(--text);
  cursor: pointer;
  font-size: 14px;
  transition: background 0.15s, border-color 0.15s;
}

.pagination button:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.pagination button.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.pagination button:disabled {
  color: var(--text-secondary);
  cursor: default;
  opacity: 0.5;
}
</style>
