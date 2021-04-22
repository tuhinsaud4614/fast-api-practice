import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Depends
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from ..schemas import UserOut
from ..utils.path import join_path
from ..utils.dependencies import get_db
from .. import models

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create", response_model=UserOut, )
def register(first_name: str, last_name: str, email: EmailStr, password: str, avatar: UploadFile = File(...), db: Session = Depends(get_db)):
    user = models.User(first_name=first_name, last_name=last_name, email=email,
                       password=password, avatar=os.path.join("images", avatar.filename))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/")
def index():
    return "tuhin"
