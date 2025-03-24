from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.models import BlogPost


async def init_database(client: AsyncIOMotorClient):
    await init_beanie(database=client.db_name, document_models=[BlogPost])
