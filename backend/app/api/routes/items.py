from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_items():
    return [{"item": "item1"}, {"item": "item2"}]
