from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # 从 database.py 导入 Base

class Category(Base):
    """文章分类模型"""
    __tablename__ = "categories"  # 数据库表名
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="分类名称")
    description = Column(String(200), nullable=True, comment="分类描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # relationship：建立一对多关系
    # "Article" 是关联的模型类名
    # back_populates="category" 表示 Article 模型中的 category 字段与之对应
    articles = relationship("Article", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

class Article(Base):
    """文章模型"""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="文章标题")
    content = Column(Text, nullable=False, comment="文章内容（Markdown格式）")
    summary = Column(String(500), nullable=True, comment="文章摘要")
    
    # 外键：关联到 categories 表的 id 字段
    # ondelete="SET NULL" 表示删除分类时，文章的外键设为 NULL（不删除文章）
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # relationship：建立多对一关系
    # 通过 article.category 可以直接访问关联的分类对象
    category = relationship("Category", back_populates="articles")
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}')>"
