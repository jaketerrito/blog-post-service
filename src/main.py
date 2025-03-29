import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.database import init_database
from src.routes import create, delete, read, update

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db_client = AsyncIOMotorClient("mongodb://root:example@mongodb:27017")
    await init_database(db_client)
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)
app.include_router(create.router)
app.include_router(read.router)
app.include_router(update.router)
app.include_router(delete.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
