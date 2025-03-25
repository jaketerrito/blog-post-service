from contextlib import asynccontextmanager

import pytest_asyncio
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from src.database import init_database
from src.main import app

AUTHOR_ID = "test_author_id"


# Configures mock mongo database
@pytest_asyncio.fixture(autouse=True)
async def database():
    client = AsyncMongoMockClient(database="test_db")
    await init_database(client)


# Configures test lifespan, prevents actual database connection
@asynccontextmanager
async def test_lifespan(app):
    yield


# Configures test client
@pytest_asyncio.fixture
async def client(database):
    app.router.lifespan_context = test_lifespan

    with TestClient(app) as test_client:
        yield test_client
