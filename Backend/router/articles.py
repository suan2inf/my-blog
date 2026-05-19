from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import ArticleUpdate,ArticleCreate,ArticleResponse
from crud import get_article,get_articles,create_article,delete_article,update_article

#创建router实例
router = APIRouter(prefix="/articles",tags=["articles"])
#post请求路由给creat
@router.post("/", response_model=ArticleResponse)
def create_new_article(
    article: ArticleCreate,
    db: Session = Depends(get_db)
):
    """创建新文章"""
    return create_article(db=db, article=article)

@router.get("/", response_model=List[ArticleResponse])
def read_articles(
    skip: int = 0,
    limit: int = 10,
    category_id: int = Query(None, description="分类ID筛选"),
    q: str = Query(None, description="搜索关键词（在标题和内容中搜索）"),
    db: Session = Depends(get_db)
):
    """获取文章列表（支持分页、分类筛选、搜索）"""
    return get_articles(
        db=db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        search=q
    )

@router.get("/{article_id}", response_model=ArticleResponse)
def read_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """获取单篇文章详情"""
    db_article = get_article(db=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    return db_article
@router.put("/{article_id}", response_model=ArticleResponse)
def update_existing_article(
    article_id: int,
    article: ArticleUpdate,
    db: Session = Depends(get_db)
):
    """更新文章"""
    db_article = update_article(db=db, article_id=article_id, article=article)
    if db_article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    return db_article
@router.delete("/{article_id}")
def delete_existing_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """删除文章"""
    db_article = delete_article(db=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    return {"message": "文章已删除"}