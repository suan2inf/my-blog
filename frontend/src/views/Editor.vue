<template>
  <div class="editor-page">
    <!-- 登录弹窗 -->
    <div class="login-overlay" v-if="showLogin">
      <div class="login-modal">
        <h2>登录</h2>
        <div class="form-group">
          <input
            v-model="username"
            type="text"
            placeholder="用户名"
            @keyup.enter="handleLogin"
          />
        </div>
        <div class="form-group">
          <input
            v-model="password"
            type="password"
            placeholder="密码"
            @keyup.enter="handleLogin"
          />
        </div>
        <p class="login-error" v-if="loginError">{{ loginError }}</p>
        <button class="btn-login" @click="handleLogin">登录</button>
      </div>
    </div>

    <!-- 编辑器 -->
    <template v-if="!showLogin">
      <h1>{{ isEdit ? '编辑文章' : '写文章' }}</h1>

      <div class="form-group">
        <input
          v-model="title"
          type="text"
          class="input-title"
          placeholder="请输入文章标题"
        />
      </div>

      <div class="form-group">
        <select v-model="categoryId" class="input-category">
          <option :value="null" disabled>选择分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <div class="form-group editor-wrapper">
        <MdEditor
          v-model="content"
          :toolbars="toolbars"
          :preview="false"
          style="min-height: 500px"
        />
      </div>

      <div class="form-actions">
        <button class="btn-primary" @click="handleSubmit" :disabled="submitting">
          {{ submitting ? '提交中...' : (isEdit ? '保存' : '发布') }}
        </button>
        <button class="btn-cancel" @click="handleCancel">取消</button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCategories, getArticle, createArticle, updateArticle } from '../api'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const route = useRoute()
const router = useRouter()

const showLogin = ref(true)
const username = ref('')
const password = ref('')
const loginError = ref('')

const isEdit = computed(() => !!route.params.id)

const title = ref('')
const content = ref('')
const categoryId = ref(null)
const categories = ref([])
const submitting = ref(false)

const toolbars = [
  'bold',
  'italic',
  'title',
  'link',
  'codeBlock',
  'orderedList',
  'unorderedList',
]

onMounted(() => {
  if (localStorage.getItem('isLoggedIn') === 'true') {
    showLogin.value = false
    initEditor()
  }
})

function handleLogin() {
  if (username.value === 'suan2inf' && password.value === '65537xqlpS') {
    localStorage.setItem('isLoggedIn', 'true')
    showLogin.value = false
    loginError.value = ''
    initEditor()
  } else {
    loginError.value = '用户名或密码错误'
  }
}

async function initEditor() {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch (e) { /* ignore */ }

  if (isEdit.value) {
    try {
      const res = await getArticle(route.params.id)
      const article = res.data
      title.value = article.title
      content.value = article.content
      categoryId.value = article.category_id
    } catch (e) {
      router.push('/')
    }
  }
}

async function handleSubmit() {
  if (!title.value.trim()) return alert('请输入文章标题')
  if (!content.value.trim()) return alert('请输入文章内容')

  submitting.value = true
  try {
    const data = {
      title: title.value.trim(),
      content: content.value,
      summary: content.value.slice(0, 150),
      category_id: categoryId.value,
    }
    if (isEdit.value) {
      await updateArticle(route.params.id, data)
      router.push(`/article/${route.params.id}`)
    } else {
      const res = await createArticle(data)
      router.push(`/article/${res.data.id}`)
    }
  } catch (e) {
    alert('操作失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

function handleCancel() {
  router.push('/')
}
</script>

<style scoped>
.editor-page { max-width: 860px; }

h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--heading);
  margin-bottom: 28px;
}

/* 登录弹窗 */
.login-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.login-modal {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 36px 32px;
  width: 360px;
  max-width: 90vw;
}

.login-modal h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 24px;
  text-align: center;
}

.login-error {
  color: #ef4444;
  font-size: 14px;
  margin-bottom: 12px;
  text-align: center;
}

.btn-login {
  width: 100%;
  padding: 10px 0;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.15s;
}
.btn-login:hover { opacity: 0.85; }

/* 表单 */
.form-group {
  margin-bottom: 20px;
}

.form-group input,
.input-category {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 15px;
  color: var(--text);
  background: var(--bg);
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
}

.form-group input:focus,
.input-category:focus {
  border-color: var(--accent);
}

.input-title {
  font-size: 18px;
  font-weight: 600;
}

.editor-wrapper {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
}

.btn-primary {
  padding: 10px 28px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.15s;
}
.btn-primary:hover { opacity: 0.85; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-cancel {
  padding: 10px 24px;
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 15px;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-cancel:hover {
  color: var(--text);
  border-color: var(--text-secondary);
}
</style>
