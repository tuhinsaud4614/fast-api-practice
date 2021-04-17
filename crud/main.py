from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    a  = 10
    return "Hello"