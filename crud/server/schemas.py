from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    avatar: str