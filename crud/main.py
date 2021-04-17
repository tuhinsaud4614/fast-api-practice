from fastapi import FastAPI
from server.routers import user

app = FastAPI()

app.include_router(user.router)