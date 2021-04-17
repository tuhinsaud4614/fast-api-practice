from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/create")
def register():
    return "create"