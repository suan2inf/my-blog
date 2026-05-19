from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import CategoryCreate,CategoryResponse
from crud import get_category,get_categories,create_category,delete_category

router = APIRouter(prefix="/categories",tags=["categories"])#实例化router
#post请求路由给创建
@router.post("/",response_model=CategoryResponse)
def creat_new_categroy(category:CategoryCreate, db:Session=Depends(get_db)):
    return create_category(db=db,name=category.name,description=category.description)

#get请求路由访问分类与访问分类列表
@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="分类不存在")
    return db_category

@router.get("/",response_model=List[CategoryResponse])
def get_some_categroies(db:Session=Depends(get_db),skip:int = 0,limit:int = 20):
    return get_categories(db=db,skip=skip,limit=limit)
#delete请求分配给delte
@router.delete("/{category_id}")
def delete_a_category(category_id:int, db:Session=Depends(get_db)):
    db_category = delete_category(db=db,category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404,detail="分类不存在")
    return {"message":"分类已删除"}