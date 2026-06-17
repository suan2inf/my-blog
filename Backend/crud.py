from sqlalchemy.orm import Session
from models import Article, Category, Project
from schemas import ArticleCreate, ArticleUpdate, ProjectCreate, ProjectUpdate
from sqlalchemy import or_

#分类CRUD
def get_category(db:Session,category_id:int):
    return db.query(Category).filter(Category.id == category_id).first()
def get_categories(db:Session,skip:int = 0,limit:int = 20):
    return db.query(Category).offset(skip).limit(limit).all()
def create_category(db:Session,name:str,description:str):
    db_category  = Category(name=name,description=description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
def delete_category(db:Session,category_id:int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category    

#文章CRUD
def get_article(db:Session,article_id:int):
    return db.query(Article).filter(Article.id == article_id).first()

def get_articles(db:Session,skip:int = 0,limit:int = 10,
                 category_id:int = None,search:str = None):
    query = db.query(Article)
    if category_id:
        query = query.filter(Article.category_id == category_id)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Article.title.ilike(search_pattern),
                Article.content.ilike(search_pattern)
            )
        )
    
    # 排序 + 分页
    return query.order_by(Article.created_at.desc()).offset(skip).limit(limit).all()    
        

def create_article(db:Session,article:ArticleCreate):
    db_article = Article(
        title = article.title,
        content = article.content,
        summary = article.summary,
        category_id = article.category_id
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
def delete_article(db:Session,article_id:int):
    db_delete = db.query(Article).filter(Article.id == article_id).first()
    if db_delete:
        db.delete(db_delete)
        db.commit()
    return db_delete
def update_article(db:Session,article_id:int,article:ArticleUpdate):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        return None
    update_data = article.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(db_article,key,value)

    db.commit()
    db.refresh(db_article)
    return db_article


# 作品 CRUD
def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    tag: str = None,
    featured: bool = None,
    search: str = None
):
    query = db.query(Project)
    if tag:
        query = query.filter(Project.tags.contains(tag))
    if featured is not None:
        query = query.filter(Project.featured == featured)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Project.title.ilike(search_pattern),
                Project.description.ilike(search_pattern),
                Project.content.ilike(search_pattern)
            )
        )
    return query.order_by(Project.sort_order.desc(), Project.created_at.desc()).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, project: ProjectCreate):
    db_project = Project(
        title=project.title,
        description=project.description,
        content=project.content,
        image_url=project.image_url,
        demo_url=project.demo_url,
        github_url=project.github_url,
        tags=project.tags,
        featured=project.featured,
        sort_order=project.sort_order
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return None
    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project