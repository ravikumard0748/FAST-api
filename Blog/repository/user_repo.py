from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
import bcrypt
from .. import models,schema
from ..database import get_db
from ..hashing import hash_password


def create_user(request : schema.User, db : Session= Depends(get_db)):
    hashed_password = hash_password(request.password)
    new_user = models.User(name = request.name , email = request.email ,
                           password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

def delete_user(id : int, db : Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"User with id {id} does not exist")
    db.delete(user)
    db.commit()
    return "deleted successfully"

def get_user(id : int, db : Session= Depends(get_db)):
    data = db.query(models.User).filter(models.User.id == id).first()
    if not data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "There is no data in this table")
    return data

def get_all_user(db : Session= Depends(get_db)):
    data = db.query(models.User).all()
    if not data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "There is no data in this table")
    return data


    
    
    