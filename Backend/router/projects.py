from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from crud import get_project, get_projects, create_project, update_project, delete_project

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """创建新作品"""
    return create_project(db=db, project=project)


@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    skip: int = 0,
    limit: int = 20,
    tag: str = Query(None, description="按标签筛选"),
    featured: bool = Query(None, description="是否只显示精选"),
    q: str = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取作品列表（支持分页、标签筛选、精选筛选、搜索）"""
    return get_projects(
        db=db,
        skip=skip,
        limit=limit,
        tag=tag,
        featured=featured,
        search=q
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """获取单个作品详情"""
    db_project = get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="作品不存在")
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_existing_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """更新作品"""
    db_project = update_project(db=db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="作品不存在")
    return db_project


@router.delete("/{project_id}")
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """删除作品"""
    db_project = delete_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="作品不存在")
    return {"message": "作品已删除"}
