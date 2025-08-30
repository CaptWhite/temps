from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services_star import process

router = APIRouter()

class StarData(BaseModel):
    starName: str
    date_time: str
    longitude: str
    latitude: str
    pressure: int
    temperature: int

@router.post("/")
async def get_star_data(data: StarData = Body(...)):
    print(data.dict())
    response = await process.main_process(data.dict())
    return JSONResponse(content={"status": "success", "data": response} )
