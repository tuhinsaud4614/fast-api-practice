import os
from uuid import uuid4, uuid1
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
import aiofiles

from ..schemas import UserOut
from ..utils.path import join_path
from ..utils.dependencies import get_db
from ..utils.password import Password
from .. import models

router = APIRouter(prefix="/user", tags=["User"])


def get_user(db: Session, email):
    return db.query(models.User).filter(models.User.email == email).first()


@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(first_name: str, last_name: str, email: EmailStr, password: str, avatar: UploadFile = File(...), db: Session = Depends(get_db)):
    user = get_user(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User already exist")

    if not avatar.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Only Image accepted like (jpg, jpeg, png etc).")

    avatar_name, avatar_ext = os.path.splitext(avatar.filename)
    new_avatar_name = f"{uuid1()}{avatar_ext}"
    new_file_path = join_path("media", "images", new_avatar_name)

    with open(new_file_path, "wb+") as image:
        content = await avatar.read()
        image.write(content)
    
    try:
        new_user = models.User(first_name=first_name, last_name=last_name, email=email,
                               password=Password.hash_password(password), avatar=f"images/{new_avatar_name}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        if os.path.isfile(new_file_path):
            os.remove(new_file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User Creation Failed")


@router.get("/")
def index():
    return "tuhin"
