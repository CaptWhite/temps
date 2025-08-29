from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    message: str

@app.get("/hello", response_model=Message)
async def read_root():
    return {"message": "Hello World!"}