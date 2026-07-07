from fastapi import APIRouter,Depends,HTTPException,status,Response
from .. import schema,models
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..repository import blog_repo

router = APIRouter(
    tags = ["Blogs"],
    prefix ="/blog"
)

@router.post("/")
def create_blog(request : schema.Blog,db : Session = Depends(get_db),status_code=status.HTTP_201_CREATED):
    return blog_repo.create(request,db)


@router.get("/",response_model = List[schema.ShowBlog])
def all(db : Session = Depends(get_db)):
    return blog_repo.all(db)



@router.get("/{id}",response_model = schema.ShowBlog)
def show(id : int,response : Response ,db : Session = Depends(get_db),status_code = 200):
    return blog_repo.show(id, response, db)


@router.delete("/{id}")
def destroy(id : int , db : Session = Depends(get_db)):
    return blog_repo.destroy(id,db)



@router.put("/{id}",status_code = status.HTTP_202_ACCEPTED)
def update(id : int , request : schema.Blog , db : Session = Depends(get_db)):
    return blog_repo.update(id,request,db)
