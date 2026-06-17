from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ==================== 分类 Schemas ====================

class CategoryBase(BaseModel):
    """分类基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    description: Optional[str] = Field(None, max_length=200, description="分类描述")

class CategoryCreate(CategoryBase):
    """创建分类的请求模型"""
    pass

class CategoryResponse(CategoryBase):
    """分类响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== 文章 Schemas ====================

class ArticleBase(BaseModel):
    """文章基础模型"""
    title: str = Field(..., min_length=1, max_length=200, description="文章标题")
    content: str = Field(..., min_length=1, description="文章内容（Markdown格式）")
    summary: Optional[str] = Field(None, max_length=500, description="文章摘要")

class ArticleCreate(ArticleBase):
    """创建文章的请求模型"""
    category_id: Optional[int] = Field(None, description="分类ID")

class ArticleUpdate(BaseModel):
    """更新文章的请求模型（所有字段可选）"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None

class ArticleResponse(ArticleBase):
    """文章响应模型（包含完整信息）"""
    id: int
    category_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ArticleWithCategory(ArticleResponse):
    """文章响应模型（包含分类详情）"""
    category: Optional[CategoryResponse] = None


# ==================== 作品 Schemas ====================

class ProjectBase(BaseModel):
    """作品基础模型"""
    title: str = Field(..., min_length=1, max_length=200, description="项目名称")
    description: str = Field(..., min_length=1, max_length=500, description="简短描述")
    content: Optional[str] = Field(None, description="详细内容（Markdown）")
    image_url: Optional[str] = Field(None, max_length=500, description="封面图URL")
    demo_url: Optional[str] = Field(None, max_length=500, description="在线演示链接")
    github_url: Optional[str] = Field(None, max_length=500, description="GitHub链接")
    tags: Optional[str] = Field(None, max_length=300, description="标签（逗号分隔）")
    featured: bool = Field(False, description="是否精选")
    sort_order: int = Field(0, description="排序权重")


class ProjectCreate(ProjectBase):
    """创建作品的请求模型"""
    pass


class ProjectUpdate(BaseModel):
    """更新作品的请求模型（所有字段可选）"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=300)
    featured: Optional[bool] = None
    sort_order: Optional[int] = None


class ProjectResponse(ProjectBase):
    """作品响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
