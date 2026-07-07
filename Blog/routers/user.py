from fastapi import APIRouter,Depends
from .. import schema
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..repository import user_repo

router = APIRouter(
    tags = ["Users"],
    prefix = "/user"
)




@router.post("/")
def create_user(request : schema.User , db : Session = Depends(get_db)):
    user_repo.create_user(request,db)



@router.delete("/{id}")
def delete_user(id : int , db : Session = Depends(get_db)):
    return user_repo.delete_user(id, db)


@router.get("/{id}",response_model = schema.ShowUser)
def get_user(id : int , db : Session = Depends(get_db)):
    return user_repo.get_user(id , db)


@router.get("/",response_model = List[schema.ShowUser])
def get_all_user(db : Session = Depends(get_db)):
    return user_repo.get_all_user(db)

