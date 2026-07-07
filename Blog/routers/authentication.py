from fastapi import APIRouter,Depends,status , HTTPException
from sqlalchemy.orm import Session
from .. import models,schema
from ..database import get_db
from ..hashing import verify_password




router = APIRouter(tags = ["Login"],prefix = "/login")

@router.post("/")
def login(request : schema.Login , db : Session = Depends(get_db)):
    user = db.query(models.User).filter(request.username == models.User.email).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Credentails Not found")
    if not verify_password(request.password,user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Incorrect Password")
    return user