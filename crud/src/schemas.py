from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    avatar: str

    class Config:
        orm_mode = True
