import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.utils.path import join_path
from src.routers import user
from src.database import Base, engine  

# Database Connection
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Static path
app.mount("/static", StaticFiles(directory=join_path("media")), name="static")

# Routes
app.include_router(user.router)
