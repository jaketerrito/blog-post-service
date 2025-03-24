from contextlib import asynccontextmanager

import pytest_asyncio
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from src.database import init_database
from src.main import app


@pytest_asyncio.fixture(autouse=True)
async def database():
    client = AsyncMongoMockClient(database="test_db")
    await init_database(client)


@asynccontextmanager
async def test_lifespan(app):
    client = AsyncMongoMockClient(database="test_db")
    await init_database(client)
    yield


@pytest_asyncio.fixture
async def client():
    app.dependency_overrides = {}
    app.router.lifespan_context = test_lifespan

    with TestClient(app) as test_client:
        yield test_client
