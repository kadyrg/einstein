from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    path="/"
)
def get_me():
    return {"Hi there"}
