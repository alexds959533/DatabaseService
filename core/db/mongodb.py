from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from core.settings import DATABASE


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorDatabase:
    return db.client[DATABASE]