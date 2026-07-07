from fastapi import HTTPException,status,Response,Depends
from .. import models,schema
from sqlalchemy.orm import Session
from ..database import get_db

 


def create(request : schema.Blog , db : Session= Depends(get_db)):
    new_blog = models.Blog(title = request.title , body = request.body,user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    
def all(db:Session= Depends(get_db)):
    blogs =db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "No data found")
    return blogs

def show(id : int, response : Response ,db : Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"Blog with the id {id} is not available")
    return blog

def update(id : int, request : schema.Blog , db : Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Blog with id {id} is not found")
    blog.update(request.model_dump())
    db.commit()
    return "updated"

def destroy(id : int, db : Session= Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return "done"
    
    