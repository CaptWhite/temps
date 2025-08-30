from fastapi import APIRouter
from fastapi import File, Form, UploadFile
from fastapi.responses import JSONResponse
import base64

from app.services_upload import process


router = APIRouter()

@router.post("/")

async def create_upload_file(
    file: UploadFile = File(...), 
    date: str = Form(...)  # Campo para el texto
):   
  img_bytesIO, csv_bytes, plate_bytes = await process.main_process(file, date)

  img_bytes = img_bytesIO.getvalue()
  img_base64 = base64.b64encode(img_bytes).decode('utf-8')
  #return StreamingResponse(img_bytes, media_type="image/jpeg")
  
  return JSONResponse(content={"imagen": img_base64, "csv": csv_bytes, "plate": plate_bytes} )