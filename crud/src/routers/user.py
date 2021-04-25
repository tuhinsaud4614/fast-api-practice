import os
import aiofiles
from uuid import uuid4, uuid1
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from typing import List

from ..schemas import UserOut, UserIn
from ..utils.path import join_path
from ..utils.dependencies import get_db
from ..utils.password import Password
from .. import models

router = APIRouter(prefix="/user", tags=["User"])


def get_user(db: Session, email):
    return db.query(models.User).filter(models.User.email == email).first()

async def upload_file_to_path(file_path, file):
    with open(file_path, "wb+") as image:
        content = await file.read()
        image.write(content)

def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


# Create User
@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(first_name: str, last_name: str, email: EmailStr, password: str, avatar: UploadFile = File(...), db: Session = Depends(get_db)):
    user = get_user(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")

    if not avatar.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only Image accepted like (jpg, jpeg, png etc).")

    avatar_name, avatar_ext = os.path.splitext(avatar.filename)
    new_avatar_name = f"{uuid1()}{avatar_ext}"
    new_file_path = join_path("media", "images", new_avatar_name)

    # with open(new_file_path, "wb+") as image:
    #     content = await avatar.read()
    #     image.write(content)
    await upload_file_to_path(new_file_path, avatar)

    try:
        new_user = models.User(first_name=first_name, last_name=last_name, email=email,
                               password=Password.hash_password(password), avatar=f"images/{new_avatar_name}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        # if os.path.isfile(new_file_path):
        #     os.remove(new_file_path)
        remove_file(new_file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User Creation Failed")


# Get all User
@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def index(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).all()
        return users
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

# Get user by id
@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def index(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

# update user
@router.patch("/{user_id}/update", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def index(user_id: int, request: UserIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    try:
        user.first_name = request.first_name
        user.last_name = request.last_name
        db.commit()
        return 
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

# update user avatar
@router.patch("/{user_id}/change-avatar", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def index(user_id: int, avatar: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    if not avatar.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only Image accepted like (jpg, jpeg, png etc).")

    avatar_name, avatar_ext = os.path.splitext(avatar.filename)
    new_avatar_name = f"{uuid1()}{avatar_ext}"
    new_file_path = join_path("media", "images", new_avatar_name)
    await upload_file_to_path(new_file_path, avatar)
    try:
        old_avatar = user.avatar
        user.avatar = f"images/{new_avatar_name}"
        db.commit()
        remove_file(join_path("media", old_avatar))
        return user
    except:
        remove_file(new_file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

# delete user
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def index(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    try:
        old_avatar = user.avatar
        old_user_id = user.id
        db.delete(user)
        db.commit()
        remove_file(join_path("media", old_avatar))
        return old_user_id
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")