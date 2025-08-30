''' from fastapi import APIRouter

router = APIRouter()

@router.post("/")

async def post_time(data: dict):
    print(data)
    return {
        "date_time_sol": data["date_time"],
        "date_time_sid": data["date_time"]
    } '''


from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services_time import process

router = APIRouter()
class StarData(BaseModel):
    date_time: str
    longitude: str
    latitude: str

@router.post("/")
async def get_star_data(data: StarData = Body(...)):
    print(data.dict())
    response = await process.main_process(data.dict())
    #return response
    return JSONResponse(content={"status": "success", "data": response} ) 
