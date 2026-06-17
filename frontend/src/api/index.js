import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
})

export function getArticles(params = {}) {
  return api.get('/articles/', { params })
}

export function getArticle(id) {
  return api.get(`/articles/${id}`)
}

export function getCategories(params = {}) {
  return api.get('/categories/', { params })
}

export function createArticle(data) {
  return api.post('/articles/', data)
}

export function updateArticle(id, data) {
  return api.put(`/articles/${id}`, data)
}

export function getProjects(params = {}) {
  return api.get('/projects/', { params })
}

export function getProject(id) {
  return api.get(`/projects/${id}`)
}

export function createProject(data) {
  return api.post('/projects/', data)
}

export function updateProject(id, data) {
  return api.put(`/projects/${id}`, data)
}

export function deleteProject(id) {
  return api.delete(`/projects/${id}`)
}
