from uuid import uuid4
from fastapi import APIRouter, UploadFile, File
from pydantic.networks import EmailStr

from ..schemas import UserOut
from ..utils import join_path

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create", response_model=UserOut)
def register(first_name: str, last_name: str, email: EmailStr, password: str, avatar: UploadFile = File(...)):
    return {
        "id": uuid4(),
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "avatar": join_path("media", "images", avatar.filename)
    }


@router.get("/")
def index():
    return "tuhin"
