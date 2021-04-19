import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.utils import join_path
from src.routers import user

app = FastAPI()

# Static path
app.mount("/static", StaticFiles(directory=join_path("media")), name="static")

# Routes
app.include_router(user.router)
