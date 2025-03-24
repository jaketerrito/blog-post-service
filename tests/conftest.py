import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient

from src.database import init_database


@pytest_asyncio.fixture(autouse=True)
async def database():
    client = AsyncMongoMockClient(database="test_db")
    await init_database(client)
