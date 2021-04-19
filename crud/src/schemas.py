from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserOut(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    avatar: str
