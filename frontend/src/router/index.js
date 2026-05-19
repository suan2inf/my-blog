import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Article from '../views/Article.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/article/:id', name: 'article', component: Article },
  { path: '/about', name: 'about', component: About },
  { path: '/editor', name: 'editor-new', component: () => import('../views/Editor.vue') },
  { path: '/editor/:id', name: 'editor-edit', component: () => import('../views/Editor.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
