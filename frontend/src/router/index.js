import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Blog from '../views/Blog.vue'
import Article from '../views/Article.vue'
import Works from '../views/Works.vue'
import WorkDetail from '../views/WorkDetail.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/blog', name: 'blog', component: Blog },
  { path: '/article/:id', name: 'article', component: Article },
  { path: '/works', name: 'works', component: Works },
  { path: '/works/:id', name: 'work-detail', component: WorkDetail },
  { path: '/about', name: 'about', component: About },
  { path: '/editor', name: 'editor-new', component: () => import('../views/Editor.vue') },
  { path: '/editor/:id', name: 'editor-edit', component: () => import('../views/Editor.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})

export default router
