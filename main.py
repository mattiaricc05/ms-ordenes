from fastapi import FastAPI
from app.database import engine, Base
from app.routers import ordenes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS-Ordenes", version="1.0.0")

app.include_router(ordenes.router)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ms-ordenes",
        "database": "postgresql"
    }