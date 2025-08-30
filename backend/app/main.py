import uvicorn
from fastapi import FastAPI, File, Form, Request, UploadFile

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import upload, items, star, scaleTime

app = FastAPI(title="Mi API REST con FastAPI")

# MIDDLEWARE #############################################
class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Leer el cuerpo como bytes
        body = await request.body()
        print(f"Solicitud: {request.method} {request.url}")
        print(f"Cuerpo: {body}")  # Decodificar si es necesario

        # Continuar con el procesamiento de la solicitud
        response = await call_next(request)
        return response

app.add_middleware(LogRequestMiddleware)

# MIDDLEWARE #############################################
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza con el origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router,  prefix="/items",  tags=["items"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(star.router, prefix="/star", tags=["star"])
app.include_router(scaleTime.router, prefix="/scaleTime", tags=["scaleTime"])



@app.get("/")
def root():
    return {"message": "Servidor Astronomy activo"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #uvicorn app.main:app --reload
