from sqlalchemy import Column, String
from uuid import uuid4

from .database import Base


def g_uuid():
    return str(uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=g_uuid)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    avatar = Column(String)
