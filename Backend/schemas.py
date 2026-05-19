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
