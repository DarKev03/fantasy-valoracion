from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import router

app = FastAPI(
    title=settings.APP_NAME,        
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
