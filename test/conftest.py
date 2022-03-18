import asyncio
from typing import  Generator
import pytest

from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from core.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from core.settings import MONGO_URL
from main import app
from core.db.mongodb import db, get_database


async def get_database_test() -> AsyncIOMotorDatabase:
    db.client = AsyncIOMotorClient(str(MONGO_URL))
    return db.client["test"]


app.dependency_overrides[get_database] = get_database_test


@pytest.fixture(scope='session')
def event_loop():
    print('loop start')
    loop = asyncio.new_event_loop()
    yield loop
    print('loop finish')
    loop.close()


async def clean_database(db):
    await db.drop_collection('files_metadata')


@pytest.fixture(scope="session", autouse=True)
async def connect():
    await connect_to_mongo()
    await db.client.drop_database('test')
    print('connect start')
    yield
    print('connect finish')
    await close_mongo_connection()


@pytest.fixture(scope="session")
def get_db() -> AsyncIOMotorDatabase:
    return db.client["test"]






