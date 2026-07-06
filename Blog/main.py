from fastapi import FastAPI,Depends,status,Response,HTTPException
from numpy import delete
from .import schema,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
import bcrypt
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/blog",tags = ['Blogs'])
def create_blog(request : schema.Blog,db : Session = Depends(get_db),status_code=status.HTTP_201_CREATED):
    new_blog = models.Blog(title = request.title , body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog",response_model = List[schema.ShowBlog],tags = ['Blogs'])
def all(db : Session = Depends(get_db)):
    blogs =db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}",response_model = schema.ShowBlog,tags = ['Blogs'])
def show(id : int,response : Response ,db : Session = Depends(get_db),status_code = 200):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available"}
    return blog

@app.delete("/blog/{id}",tags = ['Blogs'])
def destroy(id : int , db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return "done"


@app.put("/blog/{id}",status_code = status.HTTP_202_ACCEPTED,tags = ['Blogs'])
def update(id : int , request : schema.Blog , db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Blog with id {id} is not found")
    blog.update(request.model_dump())
    db.commit()
    return "updated"



@app.post("/user",tags=['Users'])
def create_user(request : schema.User , db : Session = Depends(get_db)):
    hashed_password = hash_password(request.password)
    new_user = models.User(name = request.name , email = request.email ,
                           password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.delete("/user/{id}",tags=['Users'])
def delete_user(id : int , db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"User with id {id} does not exist")
    db.delete(user)
    db.commit()
    return "deleted successfully"

def hash_password(password : str):
    b_pass = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b_pass,salt).decode("utf-8")


@app.get("/user/{id}",response_model = schema.User,tags=['Users'])
def get_user(id : int , db : Session = Depends(get_db)):
    data = db.query(models.User).filter(models.User.id == id).first()
    if not data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "There is no data in this table")
    return data


@app.get("/user",response_model = List[schema.ShowUser],tags=['Users'])
def get_all_user(db : Session = Depends(get_db),tags=['Users']):
    data = db.query(models.User).all()
    if not data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "There is no data in this table")
    return data



    