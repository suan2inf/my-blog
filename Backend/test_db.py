from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Category, Article
from datetime import datetime

def test_database():
    """验证数据库功能"""
    print("=" * 50)
    print("🧪 开始验证数据库")
    print("=" * 50)
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 1. 清理旧数据（方便重复测试）
        print("\n1️⃣ 清理旧数据...")
        db.query(Article).delete()
        db.query(Category).delete()
        db.commit()
        print("   ✅ 旧数据已清除")
        
        # 2. 创建分类
        print("\n2️⃣ 创建分类...")
        tech = Category(name="技术", description="编程、架构、工具")
        life = Category(name="生活", description="日常随笔、读书笔记")
        
        db.add(tech)
        db.add(life)
        db.commit()
        
        # 刷新获取ID
        db.refresh(tech)
        db.refresh(life)
        
        print(f"   ✅ 创建分类: {tech}")
        print(f"   ✅ 创建分类: {life}")
        
        # 3. 创建文章（关联分类）
        print("\n3️⃣ 创建文章...")
        article1 = Article(
            title="FastAPI入门指南",
            content="# FastAPI入门\n\nFastAPI是一个现代Python Web框架...",
            summary="介绍FastAPI的基本用法",
            category_id=tech.id  # 关联到技术分类
        )
        
        article2 = Article(
            title="我的2024年度总结",
            content="今年学了很多新技术...",
            summary="回顾2024年的学习历程",
            category_id=life.id  # 关联到生活分类
        )
        
        article3 = Article(
            title="SQLAlchemy最佳实践",
            content="# SQLAlchemy技巧\n\n1. 使用relationship...\n2. 注意外键约束...",
            summary="SQLAlchemy使用技巧总结",
            category_id=tech.id
        )
        
        db.add(article1)
        db.add(article2)
        db.add(article3)
        db.commit()
        
        db.refresh(article1)
        db.refresh(article2)
        db.refresh(article3)
        
        print(f"   ✅ 创建文章: {article1.title}")
        print(f"   ✅ 创建文章: {article2.title}")
        print(f"   ✅ 创建文章: {article3.title}")
        
        # 4. 测试关系查询（通过分类查文章）
        print("\n4️⃣ 查询分类下的文章（正向查询）...")
        tech_articles = db.query(Article).filter(Article.category_id == tech.id).all()
        print(f"   📁 分类【{tech.name}】下的文章:")
        for article in tech_articles:
            print(f"      - {article.title}")
        
        # 5. 测试relationship（通过文章查分类）
        print("\n5️⃣ 查询文章所属分类（反向查询，使用relationship）...")
        first_article = db.query(Article).first()
        if first_article and first_article.category:
            print(f"   📝 文章《{first_article.title}》的分类是: {first_article.category.name}")
            print(f"   💡 这是通过 article.category 直接访问的，不需要手动写join！")
        
        # 6. 测试通过relationship查文章
        print("\n6️⃣ 通过分类查文章（使用relationship）...")
        tech_with_articles = db.query(Category).filter(Category.name == "技术").first()
        if tech_with_articles:
            print(f"   📁 分类【{tech_with_articles.name}】的所有文章:")
            for article in tech_with_articles.articles:
                print(f"      - {article.title}")
            print(f"   💡 这是通过 category.articles 直接访问的！")
        
        # 7. 测试外键约束（删除分类）
        print("\n7️⃣ 测试外键约束（删除分类）...")
        print(f"   删除分类前，文章《{article1.title}》的category_id: {article1.category_id}")
        
        # 删除技术分类
        db.delete(tech)
        db.commit()
        
        # 重新查询文章，看外键是否变为NULL
        db.refresh(article1)
        print(f"   删除分类后，文章《{article1.title}》的category_id: {article1.category_id}")
        print("   ✅ 外键已自动设为NULL（文章保留，不级联删除）")
        
        # 8. 统计信息
        print("\n8️⃣ 统计信息...")
        category_count = db.query(Category).count()
        article_count = db.query(Article).count()
        print(f"   📊 当前共有 {category_count} 个分类")
        print(f"   📊 当前共有 {article_count} 篇文章")
        
        print("\n" + "=" * 50)
        print("✅ 所有验证通过！数据库工作正常")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()
