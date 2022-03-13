import asyncio
from typing import  Generator
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from core.settings import MONGO_URL
from main import app
from core.db.mongodb import db, get_database


async def get_database_test() -> AsyncIOMotorDatabase:
    return db.client["test"]


app.dependency_overrides[get_database] = get_database_test


@pytest.fixture(scope='session')
def loop():
    loop = asyncio.new_event_loop()
    return loop

@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c





@pytest.fixture(scope="session")
def conn(loop) -> Generator:
    asyncio.set_event_loop(loop)
    db.client = AsyncIOMotorClient(str(MONGO_URL))
    yield db.client["test"]
    print('final')





