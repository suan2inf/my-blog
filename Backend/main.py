from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入路由
from router.categories import router as categories_router
from router.articles import router as articles_router
from router.projects import router as projects_router

app = FastAPI(title="个人博客 API")

# 配置 CORS（跨域资源共享）
# 允许前端访问后端 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名，如 ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 注册路由
# prefix 参数为空，因为路由已经在各自文件中定义了 prefix
app.include_router(categories_router)
app.include_router(articles_router)
app.include_router(projects_router)

@app.get("/")
async def read_root():
    return {"status": "ok", "message": "个人博客后端服务运行中"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
